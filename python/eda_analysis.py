from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
EDA_DIR = REPORTS_DIR / "eda"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
EDA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("E-COMMERCE ANALYTICS PLATFORM - PYTHON EDA")
print("=" * 70)

print("\nLoading datasets...")

orders = pd.read_csv(
    PROCESSED_DIR / "order_analytics.csv"
)

order_items = pd.read_csv(
    PROCESSED_DIR / "order_item_analytics.csv"
)

print(f"Orders loaded      : {len(orders):,}")
print(f"Order items loaded : {len(order_items):,}")


# ============================================================
# DATE CONVERSION
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    if column in orders.columns:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )


# ============================================================
# BASIC DATA PROFILE
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATA PROFILE")
print("=" * 70)

print("\nOrders:")
print(orders.shape)

print("\nOrder Items:")
print(order_items.shape)

print("\nMissing values in Orders:")

missing_values = (
    orders.isnull()
    .sum()
    .sort_values(ascending=False)
)

print(
    missing_values[
        missing_values > 0
    ].head(20)
)


# ============================================================
# EXECUTIVE BUSINESS KPIs
# ============================================================

print("\n" + "=" * 70)
print("2. EXECUTIVE BUSINESS KPIs")
print("=" * 70)

total_orders = orders["order_id"].nunique()

total_customers = orders["customer_unique_id"].nunique()

total_revenue = orders["order_value"].sum()

total_freight = orders["freight_cost"].sum()

total_order_value = orders["order_total_value"].sum()

average_order_value = orders["order_total_value"].mean()

average_review = orders["review_score"].mean()

delivered_orders = orders[
    orders["is_delivered"] == 1
].copy()

late_orders = delivered_orders[
    delivered_orders["is_late"] == 1
]

late_rate = (
    len(late_orders)
    / len(delivered_orders)
    * 100
)

repeat_customer_ids = orders.loc[
    orders["is_repeat_customer"] == 1,
    "customer_unique_id"
].unique()

repeat_customers = len(
    repeat_customer_ids
)

repeat_customer_rate = (
    repeat_customers
    / total_customers
    * 100
)

print(f"Total Orders              : {total_orders:,}")
print(f"Total Customers           : {total_customers:,}")
print(f"Product Revenue           : {total_revenue:,.2f}")
print(f"Total Freight Cost        : {total_freight:,.2f}")
print(f"Total Order Value         : {total_order_value:,.2f}")
print(f"Average Order Value       : {average_order_value:,.2f}")
print(f"Average Review Score      : {average_review:.2f}")
print(f"Delivered Orders          : {len(delivered_orders):,}")
print(f"Late Orders               : {len(late_orders):,}")
print(f"Late Delivery Rate        : {late_rate:.2f}%")
print(f"Repeat Customers          : {repeat_customers:,}")
print(f"Repeat Customer Rate      : {repeat_customer_rate:.2f}%")


# ============================================================
# MONTHLY BUSINESS TREND
# ============================================================

print("\n" + "=" * 70)
print("3. MONTHLY BUSINESS TREND")
print("=" * 70)

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    orders
    .groupby("order_month")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_unique_id", "nunique"),
        revenue=("order_value", "sum"),
        freight=("freight_cost", "sum"),
        avg_order_value=("order_total_value", "mean"),
    )
    .reset_index()
)

print(
    monthly.to_string(index=False)
)

monthly.to_csv(
    EDA_DIR / "monthly_business_trend.csv",
    index=False
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly["order_month"],
    monthly["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "monthly_revenue_trend.png",
    dpi=150
)

plt.close()


# ============================================================
# MONTHLY FULFILLMENT TREND
# ============================================================

print("\n" + "=" * 70)
print("4. MONTHLY FULFILLMENT TREND")
print("=" * 70)

monthly_fulfillment = (
    delivered_orders
    .groupby(
        delivered_orders[
            "order_purchase_timestamp"
        ].dt.month
    )
    .agg(
        delivered_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delivery_delay_days", "mean"),
        avg_freight=("freight_cost", "mean"),
        avg_review=("review_score", "mean"),
    )
    .reset_index()
)

monthly_fulfillment = monthly_fulfillment.rename(
    columns={
        "order_purchase_timestamp":
            "order_month"
    }
)

monthly_fulfillment["late_delivery_rate"] = (
    monthly_fulfillment["late_orders"]
    / monthly_fulfillment["delivered_orders"]
    * 100
)

print(
    monthly_fulfillment.to_string(index=False)
)

monthly_fulfillment.to_csv(
    EDA_DIR / "monthly_fulfillment_trend.csv",
    index=False
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_fulfillment["order_month"],
    monthly_fulfillment["late_delivery_rate"],
    marker="o"
)

plt.title("Monthly Late Delivery Rate")
plt.xlabel("Purchase Month")
plt.ylabel("Late Delivery Rate (%)")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "monthly_late_delivery_rate.png",
    dpi=150
)

plt.close()


# ============================================================
# CUSTOMER PURCHASE BEHAVIOR
# ============================================================

print("\n" + "=" * 70)
print("5. CUSTOMER PURCHASE BEHAVIOR")
print("=" * 70)

customer_summary = (
    orders
    .groupby("customer_unique_id")
    .agg(
        orders=("order_id", "nunique"),
        total_value=("order_total_value", "sum"),
        avg_order_value=("order_total_value", "mean"),
        total_freight=("freight_cost", "sum"),
        last_purchase=("order_purchase_timestamp", "max"),
    )
    .reset_index()
)

customer_summary["purchase_frequency"] = (
    customer_summary["orders"]
)

frequency_distribution = (
    customer_summary["orders"]
    .value_counts()
    .sort_index()
    .reset_index()
)

frequency_distribution.columns = [
    "orders_per_customer",
    "customers"
]

print("\nPurchase frequency distribution:")

print(
    frequency_distribution.to_string(
        index=False
    )
)

frequency_distribution.to_csv(
    EDA_DIR / "customer_purchase_frequency.csv",
    index=False
)

one_time = (
    customer_summary["orders"] == 1
).sum()

repeat = (
    customer_summary["orders"] > 1
).sum()

print(f"\nOne-time customers : {one_time:,}")
print(f"Repeat customers   : {repeat:,}")


# ============================================================
# CUSTOMER VALUE SEGMENTS
# ============================================================

print("\n" + "=" * 70)
print("6. CUSTOMER VALUE SEGMENTS")
print("=" * 70)

customer_summary["value_segment"] = pd.qcut(
    customer_summary["total_value"],
    q=4,
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "Very High Value"
    ],
    duplicates="drop"
)

value_segments = (
    customer_summary
    .groupby(
        "value_segment",
        observed=False
    )
    .agg(
        customers=("customer_unique_id", "count"),
        avg_customer_value=("total_value", "mean"),
        total_customer_value=("total_value", "sum"),
        avg_orders=("orders", "mean"),
    )
    .reset_index()
)

print(
    value_segments.to_string(
        index=False
    )
)

value_segments.to_csv(
    EDA_DIR / "customer_value_segments.csv",
    index=False
)


# ============================================================
# DELIVERY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("7. DELIVERY PERFORMANCE")
print("=" * 70)

delivery_summary = (
    delivered_orders[
        [
            "delivery_days",
            "delivery_delay_days",
            "is_late",
            "freight_cost",
            "freight_ratio",
        ]
    ]
    .describe()
)

print(
    delivery_summary
)

delay_categories = pd.cut(
    delivered_orders["delivery_delay_days"],
    bins=[
        -np.inf,
        0,
        3,
        7,
        14,
        np.inf
    ],
    labels=[
        "On Time / Early",
        "1-3 Days Late",
        "4-7 Days Late",
        "8-14 Days Late",
        "15+ Days Late"
    ]
)

delay_distribution = (
    delay_categories
    .value_counts()
    .sort_index()
    .reset_index()
)

delay_distribution.columns = [
    "delay_category",
    "orders"
]

delay_distribution["percentage"] = (
    delay_distribution["orders"]
    / delay_distribution["orders"].sum()
    * 100
)

print("\nDelay distribution:")

print(
    delay_distribution.to_string(
        index=False
    )
)

delay_distribution.to_csv(
    EDA_DIR / "delivery_delay_distribution.csv",
    index=False
)


# ============================================================
# FREIGHT COST ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. FREIGHT COST ANALYSIS")
print("=" * 70)

order_value_bins = pd.cut(
    orders["order_value"],
    bins=[
        -np.inf,
        50,
        100,
        250,
        500,
        np.inf
    ],
    labels=[
        "<50",
        "50-100",
        "100-250",
        "250-500",
        "500+"
    ]
)

freight_summary = (
    orders
    .groupby(
        order_value_bins,
        observed=False
    )
    .agg(
        orders=("order_id", "nunique"),
        avg_order_value=("order_value", "mean"),
        avg_freight=("freight_cost", "mean"),
        avg_freight_ratio=("freight_ratio", "mean")
    )
    .reset_index()
)

freight_summary.columns = [
    "order_value_band",
    "orders",
    "avg_order_value",
    "avg_freight",
    "avg_freight_ratio"
]

print(
    freight_summary.to_string(
        index=False
    )
)

freight_summary.to_csv(
    EDA_DIR / "freight_by_order_value.csv",
    index=False
)


# ============================================================
# CUSTOMER SATISFACTION
# ============================================================

print("\n" + "=" * 70)
print("9. CUSTOMER SATISFACTION")
print("=" * 70)

review_distribution = (
    orders["review_score"]
    .dropna()
    .value_counts()
    .sort_index()
    .reset_index()
)

review_distribution.columns = [
    "review_score",
    "orders"
]

review_distribution["percentage"] = (
    review_distribution["orders"]
    / review_distribution["orders"].sum()
    * 100
)

print(
    review_distribution.to_string(
        index=False
    )
)

review_distribution.to_csv(
    EDA_DIR / "review_score_distribution.csv",
    index=False
)


# ------------------------------------------------------------
# SATISFACTION BY DELIVERY STATUS
# ------------------------------------------------------------

satisfaction_data = delivered_orders[
    delivered_orders["review_score"].notna()
].copy()

satisfaction_data["delivery_status"] = np.where(
    satisfaction_data["is_late"] == 1,
    "Late Delivery",
    "On-Time / Early"
)

satisfaction_by_delivery = (
    satisfaction_data
    .groupby("delivery_status")
    .agg(
        orders=("order_id", "nunique"),
        avg_review=("review_score", "mean"),
        low_satisfaction_rate=(
            "low_satisfaction",
            "mean"
        )
    )
    .reset_index()
)

satisfaction_by_delivery[
    "low_satisfaction_rate"
] *= 100

print(
    "\nSatisfaction by delivery status:"
)

print(
    satisfaction_by_delivery.to_string(
        index=False
    )
)

satisfaction_by_delivery.to_csv(
    EDA_DIR / "satisfaction_by_delivery.csv",
    index=False
)


# ============================================================
# STATE PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("10. STATE PERFORMANCE")
print("=" * 70)

state_analysis = (
    delivered_orders
    .groupby("customer_state")
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_unique_id", "nunique"),
        revenue=("order_value", "sum"),
        avg_order_value=("order_total_value", "mean"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_freight=("freight_cost", "mean"),
        avg_review=("review_score", "mean"),
    )
    .reset_index()
)

state_analysis["late_delivery_rate"] = (
    state_analysis["late_orders"]
    / state_analysis["orders"]
    * 100
)

state_analysis = state_analysis[
    state_analysis["orders"] >= 50
].sort_values(
    "late_delivery_rate",
    ascending=False
)

print(
    state_analysis.to_string(
        index=False
    )
)

state_analysis.to_csv(
    EDA_DIR / "state_fulfillment_analysis.csv",
    index=False
)


# ============================================================
# PRODUCT CATEGORY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("11. PRODUCT CATEGORY ANALYSIS")
print("=" * 70)

category_column = (
    "product_category_name_english"
)

category_analysis = (
    order_items
    .groupby(category_column)
    .agg(
        orders=("order_id", "nunique"),
        items=("order_item_id", "count"),
        revenue=("price", "sum"),
        freight=("freight_value", "sum"),
    )
    .reset_index()
)

category_analysis["total_value"] = (
    category_analysis["revenue"]
    + category_analysis["freight"]
)

category_analysis["freight_ratio"] = (
    category_analysis["freight"]
    / category_analysis["revenue"].replace(
        0,
        np.nan
    )
)

category_analysis = (
    category_analysis
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(
    category_analysis
    .head(20)
    .to_string(index=False)
)

category_analysis.to_csv(
    EDA_DIR / "product_category_analysis.csv",
    index=False
)


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("12. CORRELATION ANALYSIS")
print("=" * 70)

correlation_columns = [
    "order_value",
    "freight_cost",
    "freight_ratio",
    "delivery_days",
    "delivery_delay_days",
    "review_score",
]

correlation_data = (
    orders[
        correlation_columns
    ]
    .corr()
)

print(
    correlation_data.round(3)
)

correlation_data.to_csv(
    EDA_DIR / "correlation_matrix.csv"
)

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_data,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title(
    "Business Metric Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "correlation_matrix.png",
    dpi=150
)

plt.close()


# ============================================================
# OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("13. OUTLIER ANALYSIS")
print("=" * 70)

numeric_columns = [
    "order_value",
    "freight_cost",
    "delivery_days",
    "delivery_delay_days"
]

outlier_summary = []

for column in numeric_columns:

    data = orders[column].dropna()

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = data[
        (data < lower_bound)
        | (data > upper_bound)
    ]

    outlier_summary.append({
        "metric": column,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": len(outliers),
        "outlier_percentage": (
            len(outliers)
            / len(data)
            * 100
        )
    })

outlier_summary = pd.DataFrame(
    outlier_summary
)

print(
    outlier_summary.to_string(
        index=False
    )
)

outlier_summary.to_csv(
    EDA_DIR / "outlier_summary.csv",
    index=False
)


# ============================================================
# SAVE CUSTOMER SUMMARY
# ============================================================

customer_summary.to_csv(
    EDA_DIR / "customer_summary.csv",
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("PYTHON EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated folders:")
print(f"EDA outputs : {EDA_DIR}")
print(f"Charts      : {FIGURES_DIR}")

print("\nGenerated analysis files include:")

print(" - monthly_business_trend.csv")
print(" - monthly_fulfillment_trend.csv")
print(" - customer_purchase_frequency.csv")
print(" - customer_value_segments.csv")
print(" - delivery_delay_distribution.csv")
print(" - freight_by_order_value.csv")
print(" - review_score_distribution.csv")
print(" - satisfaction_by_delivery.csv")
print(" - state_fulfillment_analysis.csv")
print(" - product_category_analysis.csv")
print(" - correlation_matrix.csv")
print(" - outlier_summary.csv")
print(" - customer_summary.csv")

print("\nNext stage:")
print("Statistical analysis + churn-driver analysis")