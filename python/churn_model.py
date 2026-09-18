from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from sklearn.inspection import permutation_importance


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
EDA_DIR = PROJECT_ROOT / "reports" / "eda"

EDA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("E-COMMERCE ANALYTICS PLATFORM - CHURN ANALYSIS")
print("=" * 70)

print("\nLoading order analytics data...")

orders = pd.read_csv(
    PROCESSED_DIR / "order_analytics.csv"
)

print(f"Orders loaded: {len(orders):,}")


# ============================================================
# DATE CONVERSION
# ============================================================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)


# ============================================================
# CUSTOMER-LEVEL DATASET
# ============================================================
# IMPORTANT:
# The churn label already exists in order_analytics.
#
# Churn definition from the project:
# customer recency > 180 days.
#
# We DO NOT use recency as a model feature because that would
# directly leak the information used to create the churn label.
# ============================================================

print("\nBuilding customer-level analytical dataset...")

customer_data = (
    orders
    .groupby("customer_unique_id")
    .agg(
        total_orders=(
            "order_id",
            "nunique"
        ),

        total_order_value=(
            "order_total_value",
            "sum"
        ),

        avg_order_value=(
            "order_total_value",
            "mean"
        ),

        total_freight=(
            "freight_cost",
            "sum"
        ),

        avg_freight_ratio=(
            "freight_ratio",
            "mean"
        ),

        avg_delivery_days=(
            "delivery_days",
            "mean"
        ),

        late_orders=(
            "is_late",
            "sum"
        ),

        avg_review_score=(
            "review_score",
            "mean"
        ),

        low_satisfaction_orders=(
            "low_satisfaction",
            "sum"
        ),

        churned=(
            "is_churned",
            "max"
        ),
    )
    .reset_index()
)


# ============================================================
# DERIVED CUSTOMER FEATURES
# ============================================================

customer_data["late_delivery_rate"] = (
    customer_data["late_orders"]
    / customer_data["total_orders"]
)

customer_data["low_satisfaction_rate"] = (
    customer_data["low_satisfaction_orders"]
    / customer_data["total_orders"]
)


# ============================================================
# REMOVE INVALID MODEL ROWS
# ============================================================

feature_columns = [
    "total_orders",
    "total_order_value",
    "avg_order_value",
    "total_freight",
    "avg_freight_ratio",
    "avg_delivery_days",
    "late_delivery_rate",
    "avg_review_score",
    "low_satisfaction_rate",
]

model_data = customer_data[
    feature_columns + ["churned"]
].copy()

model_data = model_data.replace(
    [np.inf, -np.inf],
    np.nan
)

model_data = model_data.dropna(
    subset=feature_columns + ["churned"]
)


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("1. CUSTOMER CHURN DATASET")
print("=" * 70)

print(
    f"Customers included: {len(model_data):,}"
)

print(
    f"Churned customers : "
    f"{int(model_data['churned'].sum()):,}"
)

print(
    f"Non-churned       : "
    f"{int((model_data['churned'] == 0).sum()):,}"
)

print(
    f"Churn rate        : "
    f"{model_data['churned'].mean() * 100:.2f}%"
)


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\nChurn distribution:")

print(
    model_data["churned"]
    .value_counts()
    .sort_index()
)


# ============================================================
# FEATURES AND TARGET
# ============================================================

X = model_data[
    feature_columns
]

y = model_data[
    "churned"
].astype(int)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("2. TRAIN / TEST SPLIT")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print(
    f"Training customers : {len(X_train):,}"
)

print(
    f"Testing customers  : {len(X_test):,}"
)


# ============================================================
# LOGISTIC REGRESSION PIPELINE
# ============================================================

model = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            )
        )
    ]
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n" + "=" * 70)
print("3. TRAINING LOGISTIC REGRESSION")
print("=" * 70)

model.fit(
    X_train,
    y_train
)

print("Model training completed.")


# ============================================================
# PREDICTIONS
# ============================================================

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# MODEL PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("4. MODEL PERFORMANCE")
print("=" * 70)

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

print(
    f"Accuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")

print(cm)

confusion_df = pd.DataFrame(
    cm,
    index=[
        "Actual Non-Churn",
        "Actual Churn"
    ],
    columns=[
        "Predicted Non-Churn",
        "Predicted Churn"
    ]
)

confusion_df.to_csv(
    EDA_DIR / "churn_confusion_matrix.csv"
)


# ============================================================
# LOGISTIC REGRESSION COEFFICIENTS
# ============================================================

print("\n" + "=" * 70)
print("5. LOGISTIC REGRESSION COEFFICIENTS")
print("=" * 70)

classifier = model.named_steps[
    "classifier"
]

coefficients = classifier.coef_[0]

coefficient_df = pd.DataFrame({
    "feature": feature_columns,
    "coefficient": coefficients,
})

coefficient_df[
    "absolute_coefficient"
] = coefficient_df[
    "coefficient"
].abs()

coefficient_df[
    "direction"
] = np.where(
    coefficient_df["coefficient"] > 0,
    "Positive association with churn",
    "Negative association with churn"
)

coefficient_df = coefficient_df.sort_values(
    "absolute_coefficient",
    ascending=False
)

print(
    coefficient_df.to_string(
        index=False
    )
)

coefficient_df.to_csv(
    EDA_DIR / "churn_model_coefficients.csv",
    index=False
)


# ============================================================
# PERMUTATION IMPORTANCE
# ============================================================
# This provides a model-agnostic measure of how much model
# performance changes when each feature is shuffled.
# ============================================================

print("\n" + "=" * 70)
print("6. PERMUTATION FEATURE IMPORTANCE")
print("=" * 70)

permutation = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,
    random_state=RANDOM_STATE,
    scoring="roc_auc"
)

importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance_mean": (
        permutation.importances_mean
    ),
    "importance_std": (
        permutation.importances_std
    )
})

importance_df = importance_df.sort_values(
    "importance_mean",
    ascending=False
)

print(
    importance_df.to_string(
        index=False
    )
)

importance_df.to_csv(
    EDA_DIR / "churn_feature_importance.csv",
    index=False
)


# ============================================================
# CUSTOMER RISK SCORES
# ============================================================

print("\n" + "=" * 70)
print("7. CUSTOMER CHURN RISK SCORES")
print("=" * 70)

customer_predictions = model.predict_proba(
    X
)[:, 1]

customer_risk = model_data.copy()

customer_risk[
    "churn_probability"
] = customer_predictions

customer_risk["risk_segment"] = pd.cut(
    customer_risk["churn_probability"],
    bins=[
        -np.inf,
        0.30,
        0.60,
        np.inf
    ],
    labels=[
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ]
)

risk_summary = (
    customer_risk
    .groupby(
        "risk_segment",
        observed=False
    )
    .agg(
        customers=(
            "churned",
            "count"
        ),

        avg_churn_probability=(
            "churn_probability",
            "mean"
        ),

        actual_churn_rate=(
            "churned",
            "mean"
        ),

        avg_orders=(
            "total_orders",
            "mean"
        ),

        avg_order_value=(
            "avg_order_value",
            "mean"
        ),

        avg_delivery_days=(
            "avg_delivery_days",
            "mean"
        ),

        avg_review_score=(
            "avg_review_score",
            "mean"
        ),
    )
    .reset_index()
)

risk_summary[
    "actual_churn_rate"
] *= 100

print(
    risk_summary.to_string(
        index=False
    )
)

risk_summary.to_csv(
    EDA_DIR / "churn_risk_segments.csv",
    index=False
)


# ============================================================
# HIGH-RISK CUSTOMER PROFILE
# ============================================================

high_risk = customer_risk[
    customer_risk["risk_segment"] == "High Risk"
]

print("\nHigh-risk customer profile:")

if len(high_risk) > 0:

    print(
        f"High-risk customers : "
        f"{len(high_risk):,}"
    )

    print(
        f"Average orders      : "
        f"{high_risk['total_orders'].mean():.2f}"
    )

    print(
        f"Average order value : "
        f"{high_risk['avg_order_value'].mean():.2f}"
    )

    print(
        f"Average delivery    : "
        f"{high_risk['avg_delivery_days'].mean():.2f} days"
    )

    print(
        f"Average review      : "
        f"{high_risk['avg_review_score'].mean():.2f}"
    )

else:

    print(
        "No customers classified as High Risk."
    )


# ============================================================
# SAVE CUSTOMER-LEVEL PREDICTIONS
# ============================================================

customer_risk[
    [
        "customer_unique_id"
        if "customer_unique_id" in customer_risk.columns
        else "churned",
        "churned",
        "churn_probability",
        "risk_segment",
    ]
].to_csv(
    EDA_DIR / "customer_churn_predictions.csv",
    index=False
)


# ============================================================
# MODEL SUMMARY
# ============================================================

model_summary = pd.DataFrame([
    {
        "metric": "Accuracy",
        "value": accuracy
    },
    {
        "metric": "Precision",
        "value": precision
    },
    {
        "metric": "Recall",
        "value": recall
    },
    {
        "metric": "F1 Score",
        "value": f1
    },
    {
        "metric": "ROC-AUC",
        "value": roc_auc
    },
])

model_summary.to_csv(
    EDA_DIR / "churn_model_performance.csv",
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("CHURN ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated files:")

print(
    " - churn_model_performance.csv"
)

print(
    " - churn_model_coefficients.csv"
)

print(
    " - churn_feature_importance.csv"
)

print(
    " - churn_confusion_matrix.csv"
)

print(
    " - churn_risk_segments.csv"
)

print(
    " - customer_churn_predictions.csv"
)

print("\nNext stage:")
print("Power BI data model and dashboard development")