import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. DATABASE CONNECTION
print("Connecting to the database...")
engine = create_engine('mysql+mysqlconnector://root:YourPassword@localhost/job_market_db')

# 2. CONSOLIDATED SQL QUERY
# Using your validated CASE logic to group sub-locations
query = """
SELECT 
    CASE 
        WHEN l.location_name LIKE '%%KUALA LUMPUR%%' 
          OR l.location_name LIKE '%%BANGSAR%%' 
          OR l.location_name LIKE '%%BUKIT JALIL%%' 
          OR l.location_name LIKE '%%BANDAR TASIK SELATAN%%' THEN 'Kuala Lumpur'
        WHEN l.location_name LIKE '%%SELANGOR%%' 
          OR l.location_name LIKE '%%PETALING%%' 
          OR l.location_name LIKE '%%SHAH ALAM%%' 
          OR l.location_name LIKE '%%SUBANG%%' 
          OR l.location_name LIKE '%%SEPANG%%' 
          OR l.location_name LIKE '%%CYBERJAYA%%' 
          OR l.location_name LIKE '%%KLANG%%' 
          OR l.location_name LIKE '%%KAJANG%%' THEN 'Selangor'
        WHEN l.location_name LIKE '%%PENANG%%' 
          OR l.location_name LIKE '%%BAYAN LEPAS%%' THEN 'Penang'
        WHEN l.location_name LIKE '%%JOHOR%%' THEN 'Johor'
        ELSE l.location_name 
    END AS clean_location,
    COUNT(j.job_id) AS job_count
FROM jobs j
JOIN locations l ON j.location_id = l.location_id
WHERE (j.job_title LIKE '%%Data%%' 
   OR j.job_title LIKE '%%Machine Learning%%' 
   OR j.job_title LIKE '%% AI %%')
   AND j.job_title NOT LIKE '%%Sales%%'
   AND j.job_title NOT LIKE '%%Real Estate%%'
   AND j.job_title NOT LIKE '%%Facilities%%'
GROUP BY clean_location
ORDER BY job_count DESC
LIMIT 6;
"""
print("Executing SQL query...")
df_loc = pd.read_sql(query, con=engine)

# 3. CREATE DONUT CHART
plt.figure(figsize=(10, 8))
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

plt.pie(df_loc['job_count'],
        labels=df_loc['clean_location'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.85,
        explode=[0.05] * len(df_loc))

# Create the center circle for the donut effect
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Top AI & Data Tech Hubs in Malaysia', fontsize=16, fontweight='bold', pad=20)
plt.axis('equal')
plt.tight_layout()

plt.savefig('../outputs/location_distribution.png', dpi=300)
print("✅ Consolidated chart saved to outputs/location_distribution.png")
plt.show()