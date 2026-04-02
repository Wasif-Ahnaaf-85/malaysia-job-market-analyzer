import pandas as pd
import re
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# ==========================================
# 1. EXTRACT
# ==========================================
print("Loading dataset...")
df = pd.read_csv('../data/jobstreet_all_job_dataset.csv')

# Clean column names
df.columns = df.columns.str.strip().str.lower()
if 'listingdate' in df.columns and 'listing date' not in df.columns:
    df.rename(columns={'listingdate': 'listing date'}, inplace=True)

# ==========================================
# 2. TRANSFORM (Cleaning)
# ==========================================
print("Cleaning data...")
df.dropna(subset=['job_title', 'company', 'location'], inplace=True)
df.drop_duplicates(subset=['job_id'], inplace=True)

# --- BULLETPROOF TEXT CLEANING ---
# 1. Convert to string
# 2. Split by ANY hidden whitespace/tabs/newlines
# 3. Join back together with exactly one normal space
# 4. Convert to UPPERCASE
df['company'] = df['company'].astype(str).apply(lambda x: ' '.join(x.split())).str.upper()
df['location'] = df['location'].astype(str).apply(lambda x: ' '.join(x.split())).str.upper()
# ---------------------------------

# Clean Dates
if 'listing date' in df.columns:
    df['listing date'] = pd.to_datetime(df['listing date'], errors='coerce').dt.date

# Clean Salaries
def extract_salary(salary_text):
    if pd.isna(salary_text):
        return None, None
    numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', str(salary_text).replace(',', ''))
    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])
    elif len(numbers) == 1:
        return float(numbers[0]), float(numbers[0])
    return None, None

salary_col = 'salary' if 'salary' in df.columns else 'salaries'
if salary_col in df.columns:
    df[['min_salary', 'max_salary']] = df.apply(
        lambda row: pd.Series(extract_salary(row[salary_col])), axis=1
    )

# ==========================================
# 3. LOAD (Pushing to MySQL)
# ==========================================
print("Connecting to database...")
load_dotenv()

# Get the password securely
db_pass = os.getenv('DB_PASSWORD')

# Use it in the engine
engine = create_engine(f'mysql+mysqlconnector://root:{db_pass}@localhost/job_market_db')

print("Resetting database tables for a fresh run...")
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    # Changed to completely lowercase table names
    conn.execute(text("TRUNCATE TABLE jobs;"))
    conn.execute(text("TRUNCATE TABLE companies;"))
    conn.execute(text("TRUNCATE TABLE locations;"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    conn.commit()

print("Processing Companies and Locations...")
companies_df = pd.DataFrame(df['company'].dropna().unique(), columns=['company_name'])
locations_df = pd.DataFrame(df['location'].dropna().unique(), columns=['location_name'])

# Pushing with lowercase table names to fix the UserWarning
companies_df.to_sql('companies', con=engine, if_exists='append', index=False)
locations_df.to_sql('locations', con=engine, if_exists='append', index=False)

print("Mapping Foreign Keys...")
# Reading from lowercase table names
companies_db = pd.read_sql("SELECT company_id, company_name FROM companies", con=engine)
locations_db = pd.read_sql("SELECT location_id, location_name FROM locations", con=engine)

df = df.merge(companies_db, left_on='company', right_on='company_name', how='inner')
df = df.merge(locations_db, left_on='location', right_on='location_name', how='inner')

# Prepare final dataframe columns
final_columns = [
    'job_id', 'job_title', 'company_id', 'location_id', 'descriptions',
    'category', 'subcategory', 'role', 'type', 'salary',
    'min_salary', 'max_salary'
]
if 'listing date' in df.columns:
    final_columns.append('listing date')

existing_final_columns = [col for col in final_columns if col in df.columns]
jobs_df = df[existing_final_columns].copy()

# Rename to match SQL Schema
rename_mapping = {'type': 'job_type', 'salary': 'salary_raw'}
if 'listing date' in jobs_df.columns:
    rename_mapping['listing date'] = 'listing_date'
jobs_df.rename(columns=rename_mapping, inplace=True)

print("Pushing Jobs data to MySQL in chunks...")
# Added chunksize=1000 to prevent MySQL memory limits from crashing the pipeline
jobs_df.to_sql('jobs', con=engine, if_exists='append', index=False, chunksize=1000)

print("ETL Pipeline completed successfully! Data is now in MySQL.")