import pandas as pd
import re
from sqlalchemy import create_engine

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
print("Connecting to the database...")
# IMPORTANT: Replace 'YourPassword' with your actual MySQL password
engine = create_engine('mysql+mysqlconnector://root:Wasif#3185@localhost/job_market_db')

# Pull the job_id and the dirty salary string
query = "SELECT job_id, salary_raw FROM jobs WHERE salary_raw IS NOT NULL AND salary_raw != '';"
df_salaries = pd.read_sql(query, con=engine)


# ==========================================
# 2. THE REGEX CLEANING FUNCTION
# ==========================================
def extract_salary(salary_string):
    # Step 1: Remove commas so '3,500' becomes '3500'
    clean_string = str(salary_string).replace(',', '')

    # Step 2: Use Regex to find ALL blocks of numbers in the string
    # \d+ means "one or more digits"
    numbers = re.findall(r'\d+', clean_string)

    # Convert extracted strings to integers
    numbers = [int(num) for num in numbers]

    if len(numbers) >= 2:
        min_sal = numbers[0]
        max_sal = numbers[1]
    elif len(numbers) == 1:
        min_sal = numbers[0]
        max_sal = numbers[0]
    else:
        return pd.Series([None, None])

    # Step 3: Handle Hourly/Daily Rates (Standardizing to Monthly)
    # If the number is incredibly low (e.g., 15), it's likely hourly.
    # Let's assume 160 hours a month (40hrs * 4 weeks)
    if min_sal < 100:
        min_sal = min_sal * 160
        max_sal = max_sal * 160

    return pd.Series([min_sal, max_sal])


# ==========================================
# 3. APPLY FUNCTION AND PREVIEW
# ==========================================
print("Applying Regex cleaning...")
# Apply the function to create two new clean columns
df_salaries[['clean_min', 'clean_max']] = df_salaries['salary_raw'].apply(extract_salary)

# Filter out rows where we couldn't find any numbers
df_preview = df_salaries.dropna(subset=['clean_min', 'clean_max'])

# Print a random sample of 15 rows to compare the dirty vs clean data!
pd.set_option('display.max_colwidth', None)
print("\n--- SANITY CHECK: DIRTY VS CLEAN ---")
print(df_preview[['salary_raw', 'clean_min', 'clean_max']].sample(15))

from sqlalchemy import text

# ... (keep all your previous code above this)

# ==========================================
# 4. PUSH CLEAN DATA BACK TO MYSQL
# ==========================================
print("\nPreparing to update the database...")

# We only want to update rows where we successfully found salary numbers
df_to_update = df_salaries.dropna(subset=['clean_min', 'clean_max']).copy()

# Convert floats (e.g., 3500.0) to integers (3500) for cleaner database storage
df_to_update['clean_min'] = df_to_update['clean_min'].astype(int)
df_to_update['clean_max'] = df_to_update['clean_max'].astype(int)

# Convert the DataFrame into a list of dictionaries so SQLAlchemy can batch process it
update_data = df_to_update[['job_id', 'clean_min', 'clean_max']].to_dict('records')

# Use engine.begin() which automatically commits the transaction if successful
with engine.begin() as conn:
    # We use parameterized queries (:clean_min) to prevent SQL injection and map our dictionary keys
    update_query = text("""
                        UPDATE jobs
                        SET min_salary = :clean_min,
                            max_salary = :clean_max
                        WHERE job_id = :job_id
                        """)

    # Execute the update in a massive batch!
    conn.execute(update_query, update_data)

print(f"✅ Successfully updated {len(update_data)} job postings with clean salaries!")