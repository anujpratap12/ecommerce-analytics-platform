from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_data():
    """Load cleaned datasets."""

    customers = pd.read_csv(
        PROCESSED_DATA_DIR / "customers_clean.csv"
    )

    orders = pd.read_csv(
        PROCESSED_DATA_DIR / "orders_clean.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    order_items = pd.read_csv(
        PROCESSED_DATA_DIR / "order_items_clean.csv",
        parse_dates=["shipping_limit_date"],
    )

    payments = pd.read_csv(
        PROCESSED_DATA_DIR / "payments_clean.csv"
    )

    reviews = pd.read_csv(
        PROCESSED_DATA_DIR / "reviews_clean.csv",
        parse_dates=[
            "review_creation_date",
            "review_answer_timestamp",
        ],
    )

    products = pd.read_csv(
        PROCESSED_DATA_DIR / "products_clean.csv"
    )

    sellers = pd.read_csv(
        PROCESSED_DATA_DIR / "sellers_clean.csv"
    )

    return (
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
    )


def build_order_features(
    customers,
    orders,
    order_items,
    payments,
    reviews,
    products,
    sellers,
):
    """Create the main analytical order-level dataset."""

    # ---------------------------------------------------------
    # 1. Customer information
    # ---------------------------------------------------------

    customer_lookup = customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
    ].copy()

    orders = orders.merge(
        customer_lookup,
        on="customer_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 2. Order item aggregation
    # ---------------------------------------------------------

    item_summary = (
        order_items
        .groupby("order_id")
        .agg(
            item_count=("order_item_id", "count"),
            product_count=("product_id", "nunique"),
            seller_count=("seller_id", "nunique"),
            order_value=("price", "sum"),
            freight_cost=("freight_value", "sum"),
        )
        .reset_index()
    )

    orders = orders.merge(
        item_summary,
        on="order_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 3. Payment aggregation
    # ---------------------------------------------------------

    payment_summary = (
        payments
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_methods=("payment_type", "nunique"),
            max_installments=("payment_installments", "max"),
        )
        .reset_index()
    )

    orders = orders.merge(
        payment_summary,
        on="order_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 4. Review information
    # ---------------------------------------------------------

    review_summary = (
        reviews
        .groupby("order_id")
        .agg(
            review_score=("review_score", "mean"),
            review_count=("review_id", "nunique"),
            low_satisfaction=("is_low_satisfaction", "max"),
        )
        .reset_index()
    )

    orders = orders.merge(
        review_summary,
        on="order_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 5. Derived financial metrics
    # ---------------------------------------------------------

    orders["order_total_value"] = (
        orders["order_value"].fillna(0)
        + orders["freight_cost"].fillna(0)
    )

    orders["freight_ratio"] = np.where(
        orders["order_value"] > 0,
        orders["freight_cost"] / orders["order_value"],
        np.nan,
    )

    # Contribution proxy.
    # Olist does not contain product acquisition/COGS,
    # so this is NOT true profit.
    orders["contribution_proxy"] = (
        orders["order_value"].fillna(0)
        - orders["freight_cost"].fillna(0)
    )

    # ---------------------------------------------------------
    # 6. Delivery metrics
    # ---------------------------------------------------------

    orders["delivery_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    orders["delivery_delay_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    orders["is_delivered"] = (
        orders["order_delivered_customer_date"].notna()
    ).astype(int)

    orders["is_late"] = (
        orders["delivery_delay_days"] > 0
    ).fillna(False).astype(int)

    # ---------------------------------------------------------
    # 7. Time dimensions
    # ---------------------------------------------------------

    orders["order_date"] = (
        orders["order_purchase_timestamp"].dt.date
    )

    orders["order_year"] = (
        orders["order_purchase_timestamp"].dt.year
    )

    orders["order_month"] = (
        orders["order_purchase_timestamp"].dt.month
    )

    orders["order_month_name"] = (
        orders["order_purchase_timestamp"].dt.month_name()
    )

    orders["order_quarter"] = (
        orders["order_purchase_timestamp"].dt.quarter
    )

    orders["order_day_of_week"] = (
        orders["order_purchase_timestamp"].dt.day_name()
    )

    # ---------------------------------------------------------
    # 8. Customer purchase sequence
    # ---------------------------------------------------------

    orders = orders.sort_values(
        ["customer_unique_id", "order_purchase_timestamp"]
    )

    orders["customer_order_number"] = (
        orders.groupby("customer_unique_id")
        .cumcount()
        + 1
    )

    orders["is_repeat_customer"] = (
        orders["customer_order_number"] > 1
    ).astype(int)

    # ---------------------------------------------------------
    # 9. Customer lifetime metrics
    # ---------------------------------------------------------

    customer_lifetime = (
        orders
        .groupby("customer_unique_id")
        .agg(
            customer_lifetime_orders=(
                "order_id",
                "nunique",
            ),
            customer_lifetime_value=(
                "order_total_value",
                "sum",
            ),
            customer_avg_order_value=(
                "order_total_value",
                "mean",
            ),
            customer_total_freight=(
                "freight_cost",
                "sum",
            ),
        )
        .reset_index()
    )

    orders = orders.merge(
        customer_lifetime,
        on="customer_unique_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 10. RFM-style metrics
    # ---------------------------------------------------------

    analysis_date = (
        orders["order_purchase_timestamp"].max()
        + pd.Timedelta(days=1)
    )

    rfm = (
        orders
        .groupby("customer_unique_id")
        .agg(
            last_order_date=(
                "order_purchase_timestamp",
                "max",
            ),
            frequency=(
                "order_id",
                "nunique",
            ),
            monetary_value=(
                "order_total_value",
                "sum",
            ),
        )
        .reset_index()
    )

    rfm["recency_days"] = (
        analysis_date - rfm["last_order_date"]
    ).dt.days

    orders = orders.merge(
        rfm[
            [
                "customer_unique_id",
                "recency_days",
                "frequency",
                "monetary_value",
            ]
        ],
        on="customer_unique_id",
        how="left",
    )

    # ---------------------------------------------------------
    # 11. Churn definition
    # ---------------------------------------------------------
    # Analytical definition:
    # customers with no purchase during the final
    # 180 days of the observed dataset period.

    orders["is_churned"] = (
        orders["recency_days"] > 180
    ).astype(int)

    # ---------------------------------------------------------
    # 12. Fulfillment risk flag
    # ---------------------------------------------------------

    orders["fulfillment_risk"] = np.select(
        [
            orders["is_late"] == 1,
            orders["delivery_days"] > 14,
            orders["freight_ratio"] > 0.30,
        ],
        [
            "High",
            "High",
            "Medium",
        ],
        default="Normal",
    )

    return orders


def build_product_features(order_items, products, sellers):
    """Create item-level analytical dataset."""

    df = order_items.merge(
        products,
        on="product_id",
        how="left",
    )

    df = df.merge(
        sellers,
        on="seller_id",
        how="left",
    )

    df["item_total_value"] = (
        df["price"] + df["freight_value"]
    )

    df["freight_ratio"] = np.where(
        df["price"] > 0,
        df["freight_value"] / df["price"],
        np.nan,
    )

    return df


def save_outputs(order_features, product_features):
    """Save analytical datasets."""

    order_output = (
        PROCESSED_DATA_DIR /
        "order_analytics.csv"
    )

    product_output = (
        PROCESSED_DATA_DIR /
        "order_item_analytics.csv"
    )

    order_features.to_csv(
        order_output,
        index=False,
    )

    product_features.to_csv(
        product_output,
        index=False,
    )

    print("\nSaved:")
    print(order_output)
    print(product_output)


def main():
    print("=" * 70)
    print("BUILDING ANALYTICAL FEATURES")
    print("=" * 70)

    data = load_data()

    customers, orders, order_items, payments, reviews, products, sellers = data

    order_features = build_order_features(
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
    )

    product_features = build_product_features(
        order_items,
        products,
        sellers,
    )

    save_outputs(
        order_features,
        product_features,
    )

    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING COMPLETED")
    print("=" * 70)

    print(
        f"\nOrder analytics rows: "
        f"{len(order_features):,}"
    )

    print(
        f"Order-item analytics rows: "
        f"{len(product_features):,}"
    )

    print("\nKey analytical columns created:")
    print(
        """
- order_total_value
- freight_cost
- freight_ratio
- contribution_proxy
- delivery_days
- delivery_delay_days
- is_late
- customer_order_number
- is_repeat_customer
- customer_lifetime_orders
- customer_lifetime_value
- recency_days
- frequency
- monetary_value
- is_churned
- fulfillment_risk
"""
    )


if __name__ == "__main__":
    main()