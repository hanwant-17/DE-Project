# ================================
# RetailMart ETL Pipeline
# Author: Hanwant Singh Rathore
# ================================

import pandas as pd
import numpy as np
import sqlite3

def load_data():

    print("\nLoading CSV files...")

    sales = pd.read_csv("Data/sales_data.csv")
    products = pd.read_csv("Data/products.csv")
    stores = pd.read_csv("Data/stores.csv")

    print("CSV files loaded successfully.")

    return sales, products, stores

def clean_data(sales):

    print("\nCleaning data...")

    # Find duplicates based on business columns (ignore sale_id)
    duplicate_count = sales.duplicated(
        subset=["store_id", "product_id", "quantity", "sale_date", "amount"]
        ).sum()

    print("Duplicate Rows Found:", duplicate_count)

    # Remove duplicates
    sales = sales.drop_duplicates(
        subset=["store_id", "product_id", "quantity", "sale_date", "amount"]
    )

    print("Duplicate Rows Removed:", duplicate_count)

    sales["quantity"] = sales["quantity"].fillna(0)

    sales = sales.dropna(subset=["amount"])

    sales["sale_date"] = pd.to_datetime(
        sales["sale_date"]
    )

    sales["amount"] = sales["amount"].astype(float)

    sales["quantity"] = sales["quantity"].astype(int)

    print("Data cleaned successfully.")

    return sales

def transform_data(
        sales,
        products,
        stores):

    print("\nTransforming data...")

    merged_df = pd.merge(
        sales,
        products,
        on="product_id"
    )

    merged_df = pd.merge(
        merged_df,
        stores,
        on="store_id"
    )

    merged_df["total_revenue"] = (
        merged_df["quantity"] *
        merged_df["price"]
    )

    print("\nRevenue Statistics")

    print("Mean Revenue :", np.mean(merged_df["total_revenue"]))

    print("Maximum Revenue :", np.max(merged_df["total_revenue"]))

    print("Minimum Revenue :", np.min(merged_df["total_revenue"]))

    merged_df.to_csv(
        "Output/final_merged_data.csv",
        index=False
    )

    print("Transformation completed.")

    return merged_df

def load_to_database(merged_df):

    print("\nSaving into SQLite...")

    conn = sqlite3.connect(
        "Output/retail.db"
    )

    merged_df.to_sql(
        "retail_sales",
        conn,
        if_exists="replace",
        index=False
    )

    print("Database loaded successfully.")

    return conn

def generate_reports(
        merged_df,
        conn):

    print("\nGenerating Reports...")

    top_products = pd.read_sql("""

        SELECT
        product_name,
        SUM(quantity) AS total_quantity

        FROM retail_sales

        GROUP BY product_name

        ORDER BY total_quantity DESC

        LIMIT 3

    """, conn)



    print("\nTop Products")

    print(top_products)

    print("\nSummary Report")

    print(
        "Transactions :",
        len(merged_df)
    )

    print(
        "Revenue :",
        merged_df["total_revenue"].sum()
    )

    print(
        "Top City :",
        merged_df.groupby(
            "city"
        )["total_revenue"]
        .sum()
        .idxmax()
    )

    print(
        "Top Product :",
        merged_df.groupby(
            "product_name"
        )["quantity"]
        .sum()
        .idxmax()
    )

def run_pipeline():

    try:

        sales, products, stores = load_data()

        sales = clean_data(sales)

        merged_df = transform_data(
            sales,
            products,
            stores
        )

        conn = load_to_database(
            merged_df
        )

        generate_reports(
            merged_df,
            conn
        )

        conn.close()

        print("\nPipeline Completed Successfully.")

    except FileNotFoundError as e:

        print("\nERROR")

        print("File not found.")

        print(e)

    except Exception as e:

        print("\nUnexpected Error")

        print(e)   

if __name__ == "__main__":

    run_pipeline()