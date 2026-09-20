from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    count,
    desc,
    sum as spark_sum,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports" / "pyspark"

ORDERS_FILE = PROCESSED_DATA_DIR / "orders_clean.csv"
ORDER_ITEMS_FILE = PROCESSED_DATA_DIR / "order_items_clean.csv"

OUTPUT_FILE = REPORTS_DIR / "customer_big_data_summary.csv"


def create_spark_session():
    """Create a local Spark session for Big Data analytics."""
    return (
        SparkSession.builder
        .master("local[*]")
        .appName("OlistBigDataAnalytics")
        .getOrCreate()
    )


def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------
        # 1. Load cleaned datasets using Spark DataFrames
        # ---------------------------------------------------------
        orders = spark.read.option("header", True).option(
            "inferSchema", True
        ).csv(str(ORDERS_FILE))

        order_items = spark.read.option("header", True).option(
            "inferSchema", True
        ).csv(str(ORDER_ITEMS_FILE))

        print(f"Orders records: {orders.count()}")
        print(f"Order item records: {order_items.count()}")

        # ---------------------------------------------------------
        # 2. Select relevant columns
        # ---------------------------------------------------------
        orders_selected = orders.select(
            "order_id",
            "customer_id",
            "order_status",
            "is_late",
        )

        order_items_selected = order_items.select(
            "order_id",
            "price",
            "freight_value",
        )

        # ---------------------------------------------------------
        # 3. Join orders with order items
        # ---------------------------------------------------------
        order_summary = (
            orders_selected
            .join(
                order_items_selected,
                on="order_id",
                how="inner",
            )
            .groupBy(
                "order_id",
                "customer_id",
                "order_status",
                "is_late",
            )
            .agg(
                count("*").alias("item_count"),
                spark_sum("price").alias("total_item_value"),
                spark_sum("freight_value").alias("total_freight_value"),
                avg("price").alias("average_item_price"),
            )
        )

        print(f"Order summary records: {order_summary.count()}")

        # ---------------------------------------------------------
        # 4. Customer-level aggregation
        # ---------------------------------------------------------
        customer_summary = (
            order_summary
            .groupBy("customer_id")
            .agg(
                count("order_id").alias("order_count"),
                spark_sum("total_item_value").alias(
                    "total_item_value"
                ),
                avg("total_item_value").alias(
                    "average_order_value"
                ),
                spark_sum("total_freight_value").alias(
                    "total_freight_value"
                ),
                spark_sum("item_count").alias(
                    "total_items_purchased"
                ),
            )
            .orderBy(
                desc("total_item_value")
            )
        )

        print(f"Customer summary records: {customer_summary.count()}")

        # ---------------------------------------------------------
        # 5. Convert the final analytical result to Pandas
        #    for local CSV export.
        # ---------------------------------------------------------
        output_pdf = customer_summary.toPandas()

        # Add a deterministic spending rank after Spark aggregation.
        output_pdf["customer_spending_rank"] = (
            output_pdf["total_item_value"]
            .rank(method="min", ascending=False)
            .astype(int)
        )

        output_pdf.to_csv(
            OUTPUT_FILE,
            index=False,
        )

        print(f"\nSpark output written to: {OUTPUT_FILE}")

        # ---------------------------------------------------------
        # 6. Display top 10 customers
        # ---------------------------------------------------------
        print("\nTop 10 customers by total item value:")

        print(
            output_pdf[
                [
                    "customer_id",
                    "order_count",
                    "total_item_value",
                    "average_order_value",
                    "customer_spending_rank",
                ]
            ].head(10).to_string(index=False)
        )

    finally:
        spark.stop()


if __name__ == "__main__":
    main()