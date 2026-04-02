# malaysia-job-market-analyzer



\## Analyzing job market trends in Malaysia using Python and SQL



\## Project Overview

This project analyzes the tech, AI, and data job market in Malaysia. Using a real-world dataset of \~59,000 job postings from JobStreet, the goal is to extract actionable insights regarding in-demand skills, top hiring companies, salary distributions, and regional job availability. 



This project demonstrates an end-to-end data pipeline: extracting raw CSV data, transforming and cleaning it using Python (Pandas), loading it into a normalized MySQL database, and performing Exploratory Data Analysis (EDA).



\## Objectives

\* \*\*Data Engineering (ETL):\*\* Build a robust pipeline to clean messy text data, handle hidden whitespace, optimize memory limits via chunking, and enforce relational database integrity.

\* \*\*SQL Analysis:\*\* Query the normalized database to identify high-level market trends.

\* \*\*Exploratory Data Analysis:\*\* Use Python to visualize job distributions, tech vs. non-tech breakdowns, and salary trends.

\* \*\*Machine Learning (Future Scope):\*\* Extract specific tech stack requirements from job descriptions using NLP.



\## Tech Stack

\* \*\*Language:\*\* Python 3

\* \*\*Libraries:\*\* Pandas, SQLAlchemy, re (Regex)

\* \*\*Database:\*\* MySQL (MySQL Workbench)

\* \*\*Version Control:\*\* Git / GitHub Desktop

\* \*\*Environment:\*\* PyCharm



\## Database Schema

The raw data is parsed and normalized into three core tables to remove redundancy and enforce foreign key constraints:

1\.  `jobs` (Core job details, salary, and foreign keys)

2\.  `companies` (Unique hiring entities)

3\.  `locations` (Unique job locations)



\## Current Progress

\- \[x] \*\*Phase 1: ETL Pipeline Completed.\*\* Successfully built `src/etl\_pipeline.py` to clean raw CSV data, resolve MySQL case-sensitivity/duplicate entry clashes, and load the data into a relational schema.

\- \[ ] \*\*Phase 2 \& 3: SQL \& Python EDA.\*\* (In Progress)

\- \[ ] \*\*Phase 4: Data Visualization.\*\*

\- \[ ] \*\*Phase 5: NLP Skill Extraction.\*\*



\## Project Structure

```text

malaysia-job-market-analyzer/

│

├── data/               # Raw dataset (excluded from git)

├── notebooks/          # Jupyter notebooks / Python analysis scripts

├── src/                # Reusable modules (e.g., ETL pipeline, DB connection)

├── outputs/            # Generated charts and CSV exports

└── README.md           # Project documentation

