import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
print("Connecting to the database...")

load_dotenv()
db_pass = os.getenv('DB_PASSWORD')
engine = create_engine(f'mysql+mysqlconnector://root:{db_pass}@localhost/job_market_db')


# ==========================================
# 2. EXTRACT DATA
# ==========================================
query_top_roles = """
SELECT 
    job_title, 
    COUNT(job_id) as demand
FROM jobs
WHERE (job_title LIKE '%Data%' 
   OR job_title LIKE '%Machine Learning%' 
   OR job_title LIKE '% AI %' 
   OR job_title LIKE '%Artificial Intelligence%')
   AND job_title NOT LIKE '%Entry%'
   AND job_title NOT LIKE '%Clerk%'
   AND job_title NOT LIKE '%Admin%'
GROUP BY job_title
ORDER BY demand DESC
LIMIT 15;
"""

print("Executing SQL query...")
df_roles = pd.read_sql(query_top_roles, con=engine)

# ==========================================
# 3. DATA VISUALIZATION
# ==========================================
print("Generating visualization...")

# Sort the dataframe ascending so the biggest bar ends up at the top of the chart
df_roles = df_roles.sort_values(by='demand', ascending=True)

# Create the figure and axes objects
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(df_roles['job_title'], df_roles['demand'], color='#1f77b4')
ax.set_title('Top 15 High-Demand AI & Data Roles in Malaysia', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Job Postings', fontsize=12)
ax.set_ylabel('Job Title', fontsize=12)
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.bar_label(bars, padding=5, fontsize=11)
plt.tight_layout()

# Save and show
plt.savefig('../outputs/top_ai_data_roles.png', dpi=300)
print("Chart saved to outputs/top_ai_data_roles.png")
plt.show()