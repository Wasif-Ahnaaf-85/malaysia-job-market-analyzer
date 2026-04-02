import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
print("Connecting to the database...")
# IMPORTANT: Replace 'YourPassword' with your actual MySQL password
engine = create_engine('mysql+mysqlconnector://root:Wasif#3185@localhost/job_market_db')

# ==========================================
# 2. EXTRACT DATA USING A "SMART" SQL QUERY
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
# 3. DATA VISUALIZATION (PURE MATPLOTLIB)
# ==========================================
print("Generating visualization...")

# Sort the dataframe ascending so the biggest bar ends up at the top of the chart
df_roles = df_roles.sort_values(by='demand', ascending=True)

# Create the figure and axes objects
fig, ax = plt.subplots(figsize=(12, 8))

# Draw the horizontal bar chart
bars = ax.barh(df_roles['job_title'], df_roles['demand'], color='#1f77b4') # Standard Matplotlib blue

# Add titles and labels
ax.set_title('Top 15 High-Demand AI & Data Roles in Malaysia', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Job Postings', fontsize=12)
ax.set_ylabel('Job Title', fontsize=12)

# Add gridlines behind the bars for easier reading
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Add the exact numbers to the end of each bar
ax.bar_label(bars, padding=5, fontsize=11)

# Ensure nothing gets cut off
plt.tight_layout()

# Save and show
plt.savefig('../outputs/top_ai_data_roles.png', dpi=300)
print("Chart saved to outputs/top_ai_data_roles.png")
plt.show()