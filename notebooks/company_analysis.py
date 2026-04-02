import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
print("Connecting to the database...")
engine = create_engine('mysql+mysqlconnector://root:YourPassword@localhost/job_market_db')

# ==========================================
# 2. SQL QUERY
# ==========================================
query = """
SELECT 
    CASE 
        WHEN c.company_name LIKE '%%Intel%%' THEN 'Intel'
        WHEN c.company_name LIKE '%%Deloitte%%' THEN 'Deloitte'
        WHEN c.company_name LIKE '%%Huawei%%' THEN 'Huawei'
        WHEN c.company_name LIKE '%%Maybank%%' THEN 'Maybank'
        WHEN c.company_name LIKE '%%Accenture%%' THEN 'Accenture'
        WHEN c.company_name LIKE '%%Michael Page%%' THEN 'Michael Page (Recruitment)'
        ELSE c.company_name 
    END AS clean_company,
    COUNT(j.job_id) AS open_roles
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
WHERE (j.job_title LIKE '%%Data%%' 
   OR j.job_title LIKE '%%Machine Learning%%' 
   OR j.job_title LIKE '%% AI %%')
   AND c.company_name NOT LIKE '%%SEEK%%'
   AND c.company_name NOT LIKE '%%Private Advertiser%%'
   AND c.company_name NOT LIKE '%%AGENSI PEKERJAAN%%'
GROUP BY clean_company
ORDER BY open_roles DESC
LIMIT 10;
"""

print("Executing SQL query...")
df_comp = pd.read_sql(query, con=engine)

# ==========================================
# 3. CREATE BAR CHART
# ==========================================
print("Generating visualization...")

plt.figure(figsize=(12, 8))

# Sort ascending so the #1 company appears at the top of the chart
df_comp = df_comp.sort_values(by='open_roles', ascending=True)

# Create the horizontal bars
bars = plt.barh(df_comp['clean_company'], df_comp['open_roles'], color='#17becf', edgecolor='black')

# Titles and formatting
plt.title('Top 10 Hiring Companies for AI & Data in Malaysia', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Open Roles', fontsize=12)
plt.ylabel('Company', fontsize=12)

# Add data labels directly onto the bars
plt.bar_label(bars, padding=5, fontsize=11, fontweight='bold')

# Extend X-axis slightly so the labels don't get cut off
plt.xlim(0, df_comp['open_roles'].max() * 1.15)

# Add grid lines behind the bars for easier reading
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

# Save and show
plt.savefig('../outputs/top_employers.png', dpi=300)
print("✅ Chart saved to outputs/top_employers.png")
plt.show()