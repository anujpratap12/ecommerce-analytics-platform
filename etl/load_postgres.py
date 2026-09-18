from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Allow imports from the project root
sys.path.insert(0, str(PROJECT_ROOT))

from python.db_connection import engine


PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# PostgreSQL schema setup
# ---------------------------------------------------------

def create_schemas():
    """Ensure required PostgreSQL schemas exist."""

    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS raw;")
        )

        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS staging;")
        )

        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS analytics;")
        )

    print("PostgreSQL schemas verified.")


# ---------------------------------------------------------
# CSV → PostgreSQL loader
# ---------------------------------------------------------

def load_table(file_name, table_name, schema):
    """Load a processed CSV file into a PostgreSQL table."""

    file_path = PROCESSED_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    print(
        f"\nLoading {file_name} "
        f"-> {schema}.{table_name}"
    )

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    print(
        f"Loaded {len(df):,} rows "
        f"into {schema}.{table_name}"
    )


# ---------------------------------------------------------
# Main ETL process
# ---------------------------------------------------------

def main():
    print("=" * 70)
    print("POSTGRESQL DATA INGESTION")
    print("=" * 70)

    # Make sure schemas exist
    create_schemas()

    # -----------------------------------------------------
    # Staging tables
    # -----------------------------------------------------

    print("\n--- Loading staging tables ---")

    load_table(
        "customers_clean.csv",
        "customers",
        "staging",
    )

    load_table(
        "sellers_clean.csv",
        "sellers",
        "staging",
    )

    load_table(
        "products_clean.csv",
        "products",
        "staging",
    )

    load_table(
        "orders_clean.csv",
        "orders",
        "staging",
    )

    load_table(
        "order_items_clean.csv",
        "order_items",
        "staging",
    )

    load_table(
        "payments_clean.csv",
        "payments",
        "staging",
    )

    load_table(
        "reviews_clean.csv",
        "reviews",
        "staging",
    )

    # -----------------------------------------------------
    # Analytics tables
    # -----------------------------------------------------

    print("\n--- Loading analytics tables ---")

    load_table(
        "order_analytics.csv",
        "order_analytics",
        "analytics",
    )

    load_table(
        "order_item_analytics.csv",
        "order_item_analytics",
        "analytics",
    )

    # -----------------------------------------------------
    # Completion
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("POSTGRESQL INGESTION COMPLETED")
    print("=" * 70)

    print("\nSchemas:")
    print("  staging")
    print("  analytics")

    print("\nStaging tables:")
    print("  staging.customers")
    print("  staging.sellers")
    print("  staging.products")
    print("  staging.orders")
    print("  staging.order_items")
    print("  staging.payments")
    print("  staging.reviews")

    print("\nAnalytics tables:")
    print("  analytics.order_analytics")
    print("  analytics.order_item_analytics")


# ---------------------------------------------------------
# Script entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()