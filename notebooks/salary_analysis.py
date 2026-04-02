import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
print("Connecting to the database...")
# Load the variables from the .env file
load_dotenv()

# Get the password securely
db_pass = os.getenv('DB_PASSWORD')

# Use it in the engine
engine = create_engine(f'mysql+mysqlconnector://root:{db_pass}@localhost/job_market_db')
# ==========================================
# 2. EXTRACT CLEAN SALARY DATA
# ==========================================
query_salaries = """
SELECT 
    job_title, 
    ROUND(AVG(min_salary), 0) AS avg_min_salary,
    ROUND(AVG(max_salary), 0) AS avg_max_salary
FROM jobs
WHERE (job_title LIKE '%Data%' 
   OR job_title LIKE '%Machine Learning%' 
   OR job_title LIKE '% AI %' 
   OR job_title LIKE '%Artificial Intelligence%')
   AND job_title NOT LIKE '%Entry%'
   AND job_title NOT LIKE '%Clerk%'
   AND job_title NOT LIKE '%Admin%'
   AND job_title NOT LIKE '%Sales%'
   AND job_title NOT LIKE '%Real Estate%'
   AND job_title NOT LIKE '%Property%'
   AND job_title NOT LIKE '%Datacom%'
   AND job_title NOT LIKE '%Procurement%'
   AND job_title NOT LIKE '%Facilities%'    -- NEW
   AND job_title NOT LIKE '%Center%'        -- NEW
   AND job_title NOT LIKE '%Centre%'        -- NEW
   AND min_salary IS NOT NULL 
   AND min_salary > 0
GROUP BY job_title
HAVING COUNT(job_id) > 1
ORDER BY avg_max_salary DESC
LIMIT 10;
"""

print("Executing SQL query...")
df_salary = pd.read_sql(query_salaries, con=engine)

# ==========================================
# 3. DATA VISUALIZATION (PURE MATPLOTLIB)
# ==========================================
print("Generating visualization...")

# Sort ascending so the highest paying jobs appear at the top
df_salary = df_salary.sort_values(by='avg_max_salary', ascending=True)

# Create figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Set up the positions for the grouped bars
y = np.arange(len(df_salary['job_title']))
height = 0.35

# Draw the bars
rects1 = ax.barh(y - height/2, df_salary['avg_min_salary'], height, label='Avg Min Salary (RM)', color='#1f77b4')
rects2 = ax.barh(y + height/2, df_salary['avg_max_salary'], height, label='Avg Max Salary (RM)', color='#ff7f0e')

# Add titles and labels
ax.set_title('Average Salary Ranges for Top AI/Data Roles in Malaysia', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Monthly Salary (MYR)', fontsize=12)
ax.set_ylabel('Job Title', fontsize=12)

# Set the y-axis ticks
ax.set_yticks(y)
ax.set_yticklabels(df_salary['job_title'])

# Add legend and grid
ax.legend(loc='lower right')
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Format the numbers on the bars
ax.bar_label(rects1, padding=5, fmt='{:,.0f}', fontsize=10)
ax.bar_label(rects2, padding=5, fmt='{:,.0f}', fontsize=10)

# THE FIX: Extend the X-axis limit by 15% so the text doesn't get cut off!
max_salary_value = df_salary['avg_max_salary'].max()
ax.set_xlim(0, max_salary_value * 1.15)

# Ensure nothing gets cut off
plt.tight_layout()

# Save and show
plt.savefig('../outputs/salary_ranges.png', dpi=300)
print("Chart saved to outputs/salary_ranges.png")
plt.show()