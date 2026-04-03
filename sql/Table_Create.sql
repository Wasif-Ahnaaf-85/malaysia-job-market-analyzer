CREATE DATABASE job_market_db;
USE job_market_db;

CREATE TABLE Companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Jobs (
    job_id VARCHAR(50) PRIMARY KEY, 
    job_title VARCHAR(255) NOT NULL,
    company_id INT,
    location_id INT,
    descriptions TEXT, 
    category VARCHAR(100),
    subcategory VARCHAR(100),
    role VARCHAR(100),
    job_type VARCHAR(100), 
    salary_raw VARCHAR(255),  
    min_salary DECIMAL(10, 2), 
    max_salary DECIMAL(10, 2),
    listing_date DATE,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);