from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def clean_customers():
    file = RAW_DATA_DIR / "olist_customers_dataset.csv"
    df = pd.read_csv(file)

    # Standardize text fields
    df["customer_city"] = df["customer_city"].str.strip().str.lower()
    df["customer_state"] = df["customer_state"].str.strip().str.upper()

    # Remove exact duplicate records
    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "customers_clean.csv"
    df.to_csv(output, index=False)

    print(f"Customers: {len(df):,} rows")


def clean_geolocation():
    file = RAW_DATA_DIR / "olist_geolocation_dataset.csv"
    df = pd.read_csv(file)

    df["geolocation_city"] = (
        df["geolocation_city"]
        .str.strip()
        .str.lower()
    )

    df["geolocation_state"] = (
        df["geolocation_state"]
        .str.strip()
        .str.upper()
    )

    # Remove exact duplicate records
    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "geolocation_clean.csv"
    df.to_csv(output, index=False)

    print(f"Geolocation: {len(df):,} rows")


def clean_order_items():
    file = RAW_DATA_DIR / "olist_order_items_dataset.csv"
    df = pd.read_csv(file)

    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    # Basic numeric validation
    df = df[
        (df["price"] >= 0) &
        (df["freight_value"] >= 0)
    ]

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "order_items_clean.csv"
    df.to_csv(output, index=False)

    print(f"Order items: {len(df):,} rows")


def clean_payments():
    file = RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    df = pd.read_csv(file)

    df["payment_type"] = (
        df["payment_type"]
        .str.strip()
        .str.lower()
    )

    df = df[
        (df["payment_value"] >= 0) &
        (df["payment_installments"] >= 0)
    ]

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "payments_clean.csv"
    df.to_csv(output, index=False)

    print(f"Payments: {len(df):,} rows")


def clean_reviews():
    file = RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
    df = pd.read_csv(file)

    df["review_creation_date"] = pd.to_datetime(
        df["review_creation_date"],
        errors="coerce"
    )

    df["review_answer_timestamp"] = pd.to_datetime(
        df["review_answer_timestamp"],
        errors="coerce"
    )

    # Normalize review text
    for column in [
        "review_comment_title",
        "review_comment_message"
    ]:
        df[column] = df[column].fillna("").str.strip()

    # Satisfaction indicator
    df["is_low_satisfaction"] = (
        df["review_score"] <= 2
    ).astype(int)

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "reviews_clean.csv"
    df.to_csv(output, index=False)

    print(f"Reviews: {len(df):,} rows")


def clean_orders():
    file = RAW_DATA_DIR / "olist_orders_dataset.csv"
    df = pd.read_csv(file)

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    # Delivery status
    df["is_delivered"] = (
        df["order_status"] == "delivered"
    ).astype(int)

    # Delivery days
    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    # Delivery delay compared with estimated date
    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    # Late delivery flag
    df["is_late"] = (
        df["delivery_delay_days"] > 0
    ).fillna(False).astype(int)

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "orders_clean.csv"
    df.to_csv(output, index=False)

    print(f"Orders: {len(df):,} rows")


def clean_products():
    file = RAW_DATA_DIR / "olist_products_dataset.csv"
    translation_file = (
        RAW_DATA_DIR /
        "product_category_name_translation.csv"
    )

    df = pd.read_csv(file)
    translation = pd.read_csv(translation_file)

    # Translate product categories
    df = df.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    df["product_category_name_english"] = (
        df["product_category_name_english"]
        .fillna("unknown")
        .str.strip()
        .str.lower()
    )

    # Missing numeric product attributes
    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "products_clean.csv"
    df.to_csv(output, index=False)

    print(f"Products: {len(df):,} rows")


def clean_sellers():
    file = RAW_DATA_DIR / "olist_sellers_dataset.csv"
    df = pd.read_csv(file)

    df["seller_city"] = (
        df["seller_city"]
        .str.strip()
        .str.lower()
    )

    df["seller_state"] = (
        df["seller_state"]
        .str.strip()
        .str.upper()
    )

    df = df.drop_duplicates()

    output = PROCESSED_DATA_DIR / "sellers_clean.csv"
    df.to_csv(output, index=False)

    print(f"Sellers: {len(df):,} rows")


def main():
    print("=" * 70)
    print("STARTING DATA CLEANING")
    print("=" * 70)

    clean_customers()
    clean_geolocation()
    clean_order_items()
    clean_payments()
    clean_reviews()
    clean_orders()
    clean_products()
    clean_sellers()

    print("\n" + "=" * 70)
    print("DATA CLEANING COMPLETED")
    print("=" * 70)

    print(f"\nProcessed files saved to:")
    print(PROCESSED_DATA_DIR)


if __name__ == "__main__":
    main()