# DE-Project
# RetailMart ETL Data Pipeline

## Project Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline using Python, Pandas, NumPy, and SQLite.

The pipeline reads retail sales data from CSV files, cleans and transforms the data, loads it into a SQLite database, and generates reports for business analysis.

## Technologies Used

* Python
* Pandas
* NumPy
* SQLite
* VS Code
* Git & GitHub

## Project Structure

```
DE Project/
│
├── data/
│   ├── sales_data.csv
│   ├── products.csv
│   └── stores.csv
│
├── output/
│   ├── retail.db
│   └── final_merged_data.csv
│
├── retail_pipeline.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
```

## Features

* Load data from multiple CSV files
* Remove duplicate records
* Handle missing values
* Convert data types
* Merge datasets using Pandas
* Calculate total revenue
* Generate business insights
* Store processed data in SQLite
* Execute SQL queries for reporting
* Modular ETL pipeline with error handling

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the pipeline:

```bash
python retail_pipeline.py
```

## Sample Output

* CSV files loaded successfully
* Duplicate records removed
* Revenue statistics generated
* SQLite database created
* SQL reports executed
* Summary report displayed

## Author

Hanwant Singh Rathore
