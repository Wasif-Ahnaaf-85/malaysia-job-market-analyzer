import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
load_dotenv()
db_pass = os.getenv('DB_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://root:{db_pass}@localhost/job_market_db')

# ==========================================
# 2. DEFINE TABLES AND FOLDER
# ==========================================
tables_to_export = ['companies', 'jobs', 'locations']
output_dir = '../data'

# Automatically create the 'data' folder if it doesn't exist yet
os.makedirs(output_dir, exist_ok=True)

# ==========================================
# 3. EXTRACT AND EXPORT (ETL LOOP)
# ==========================================
print("Starting data export process...\n" + "-" * 30)

for table in tables_to_export:
    print(f" Extracting '{table}' table...")

    # Query the full table
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, con=engine)

    output_path = f"{output_dir}/{table}_export.csv"
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f" Saved {len(df)} rows to {output_path}")

print("-" * 30 + "\n All tables successfully exported!")