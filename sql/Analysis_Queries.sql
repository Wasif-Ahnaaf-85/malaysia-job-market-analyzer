-- Entry Counts 
SELECT 'Jobs' AS category, COUNT(*) AS total_count FROM jobs
UNION ALL
SELECT 'Companies', COUNT(*) FROM companies
UNION ALL
SELECT 'Locations', COUNT(*) FROM locations;


-- Top 10 Hiring Companies
SELECT 
    c.company_name, 
    COUNT(j.job_id) AS job_posting_count
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
GROUP BY c.company_name
ORDER BY job_posting_count DESC
LIMIT 10;

-- Finding the AI/Data Roles 
SELECT 
    job_title, 
    COUNT(job_id) as demand
FROM jobs
WHERE job_title LIKE '%Data%' 
   OR job_title LIKE '%Machine Learning%' 
   OR job_title LIKE '% AI %' 
   OR job_title LIKE '%Artificial Intelligence%'
GROUP BY job_title
ORDER BY demand DESC
LIMIT 15;

-- Salary Analysis (Averages by Role)
SELECT 
    job_title, 
    COUNT(job_id) AS postings_with_salary,
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
   AND min_salary IS NOT NULL 
   AND min_salary > 0
GROUP BY job_title
ORDER BY postings_with_salary DESC
LIMIT 10; 

-- Location Analysis
SELECT 
    CASE 
        -- Group all KL variations and neighborhoods
        WHEN l.location_name LIKE '%KUALA LUMPUR%' 
          OR l.location_name LIKE '%BANGSAR%' 
          OR l.location_name LIKE '%BUKIT JALIL%' 
          OR l.location_name LIKE '%BANDAR TASIK SELATAN%' THEN 'Kuala Lumpur'
        
        -- Group all Selangor districts (Petaling, Subang, etc.)
        WHEN l.location_name LIKE '%SELANGOR%' 
          OR l.location_name LIKE '%PETALING%' 
          OR l.location_name LIKE '%SHAH ALAM%' 
          OR l.location_name LIKE '%SUBANG%' 
          OR l.location_name LIKE '%SEPANG%' 
          OR l.location_name LIKE '%CYBERJAYA%' 
          OR l.location_name LIKE '%KLANG%' 
          OR l.location_name LIKE '%KAJANG%' THEN 'Selangor'
        
        -- Group Penang variations
        WHEN l.location_name LIKE '%PENANG%' 
          OR l.location_name LIKE '%BAYAN LEPAS%' THEN 'Penang'
        
        -- Group Johor variations
        WHEN l.location_name LIKE '%JOHOR%' THEN 'Johor'
        
        ELSE l.location_name 
    END AS clean_location,
    COUNT(j.job_id) AS job_count
FROM jobs j
JOIN locations l ON j.location_id = l.location_id
WHERE (j.job_title LIKE '%Data%' 
   OR j.job_title LIKE '%Machine Learning%' 
   OR j.job_title LIKE '% AI %' 
   OR j.job_title LIKE '%Artificial Intelligence%')
   AND j.job_title NOT LIKE '%Entry%'
   AND j.job_title NOT LIKE '%Clerk%'
   AND j.job_title NOT LIKE '%Admin%'
   AND j.job_title NOT LIKE '%Sales%'
   AND j.job_title NOT LIKE '%Facilities%'
   AND j.job_title NOT LIKE '%Center%'
   AND j.job_title NOT LIKE '%Centre%'
GROUP BY clean_location
ORDER BY job_count DESC
LIMIT 5;

-- Employer Analysis 
SELECT 
    CASE 
        WHEN c.company_name LIKE '%Intel%' THEN 'Intel'
        WHEN c.company_name LIKE '%Deloitte%' THEN 'Deloitte'
        WHEN c.company_name LIKE '%Huawei%' THEN 'Huawei'
        WHEN c.company_name LIKE '%Maybank%' THEN 'Maybank'
        WHEN c.company_name LIKE '%Accenture%' THEN 'Accenture'
        WHEN c.company_name LIKE '%Michael Page%' THEN 'Michael Page (Recruitment)'
        ELSE c.company_name 
    END AS clean_company,
    COUNT(j.job_id) AS open_roles,
    ROUND(AVG(j.max_salary), 0) AS avg_max_salary
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
WHERE (j.job_title LIKE '%Data%' 
   OR j.job_title LIKE '%Machine Learning%' 
   OR j.job_title LIKE '% AI %')
   -- Filter out SEEK since it's the job platform, not the employer
   AND c.company_name NOT LIKE '%SEEK%'
   AND c.company_name NOT LIKE '%Private Advertiser%'
   AND c.company_name NOT LIKE '%%Agensi Pekerjaan%%'
GROUP BY clean_company
ORDER BY open_roles DESC
LIMIT 10;