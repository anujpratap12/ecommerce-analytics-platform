from pathlib import Path

import pandas as pd
import numpy as np
from scipy import stats


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
EDA_DIR = PROJECT_ROOT / "reports" / "eda"

EDA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("E-COMMERCE ANALYTICS PLATFORM - STATISTICAL ANALYSIS")
print("=" * 70)

print("\nLoading data...")

orders = pd.read_csv(
    PROCESSED_DIR / "order_analytics.csv"
)

print(f"Orders loaded: {len(orders):,}")


# ============================================================
# BASIC PREPARATION
# ============================================================

numeric_columns = [
    "order_value",
    "order_total_value",
    "freight_cost",
    "freight_ratio",
    "delivery_days",
    "delivery_delay_days",
    "review_score",
]

for column in numeric_columns:
    if column in orders.columns:
        orders[column] = pd.to_numeric(
            orders[column],
            errors="coerce"
        )


# ============================================================
# HELPER FUNCTION
# ============================================================

def confidence_interval_mean(data, confidence=0.95):
    """
    Calculate confidence interval for the mean.
    """

    data = pd.Series(data).dropna()

    n = len(data)

    mean = data.mean()

    standard_error = stats.sem(data)

    margin = (
        standard_error
        * stats.t.ppf(
            (1 + confidence) / 2,
            n - 1
        )
    )

    return (
        mean - margin,
        mean + margin
    )


# ============================================================
# RESULTS STORAGE
# ============================================================

results = []


# ============================================================
# 1. DELIVERY DAYS VS REVIEW SCORE
# ============================================================

print("\n" + "=" * 70)
print("1. DELIVERY DAYS VS REVIEW SCORE")
print("=" * 70)

data = orders[
    [
        "delivery_days",
        "review_score"
    ]
].dropna()

pearson_r, pearson_p = stats.pearsonr(
    data["delivery_days"],
    data["review_score"]
)

spearman_rho, spearman_p = stats.spearmanr(
    data["delivery_days"],
    data["review_score"]
)

print(f"Sample size          : {len(data):,}")
print(f"Pearson correlation  : {pearson_r:.4f}")
print(f"Pearson p-value      : {pearson_p:.6f}")
print(f"Spearman correlation : {spearman_rho:.4f}")
print(f"Spearman p-value     : {spearman_p:.6f}")

results.append({
    "analysis": "Delivery Days vs Review Score",
    "test": "Pearson correlation",
    "sample_size": len(data),
    "statistic": pearson_r,
    "p_value": pearson_p,
    "effect_size": pearson_r,
    "interpretation": (
        "Negative association between delivery duration "
        "and review score"
    )
})


# ============================================================
# 2. DELIVERY DELAY VS REVIEW SCORE
# ============================================================

print("\n" + "=" * 70)
print("2. DELIVERY DELAY VS REVIEW SCORE")
print("=" * 70)

data = orders[
    [
        "delivery_delay_days",
        "review_score"
    ]
].dropna()

pearson_r, pearson_p = stats.pearsonr(
    data["delivery_delay_days"],
    data["review_score"]
)

spearman_rho, spearman_p = stats.spearmanr(
    data["delivery_delay_days"],
    data["review_score"]
)

print(f"Sample size          : {len(data):,}")
print(f"Pearson correlation  : {pearson_r:.4f}")
print(f"Pearson p-value      : {pearson_p:.6f}")
print(f"Spearman correlation : {spearman_rho:.4f}")
print(f"Spearman p-value     : {spearman_p:.6f}")

results.append({
    "analysis": "Delivery Delay vs Review Score",
    "test": "Pearson correlation",
    "sample_size": len(data),
    "statistic": pearson_r,
    "p_value": pearson_p,
    "effect_size": pearson_r,
    "interpretation": (
        "Negative association between delivery delay "
        "and review score"
    )
})


# ============================================================
# 3. FREIGHT COST VS ORDER VALUE
# ============================================================

print("\n" + "=" * 70)
print("3. FREIGHT COST VS ORDER VALUE")
print("=" * 70)

data = orders[
    [
        "order_value",
        "freight_cost"
    ]
].dropna()

pearson_r, pearson_p = stats.pearsonr(
    data["order_value"],
    data["freight_cost"]
)

print(f"Sample size         : {len(data):,}")
print(f"Pearson correlation : {pearson_r:.4f}")
print(f"p-value             : {pearson_p:.6f}")

results.append({
    "analysis": "Freight Cost vs Order Value",
    "test": "Pearson correlation",
    "sample_size": len(data),
    "statistic": pearson_r,
    "p_value": pearson_p,
    "effect_size": pearson_r,
    "interpretation": (
        "Positive association between order value "
        "and freight cost"
    )
})


# ============================================================
# 4. FREIGHT RATIO VS ORDER VALUE
# ============================================================

print("\n" + "=" * 70)
print("4. FREIGHT RATIO VS ORDER VALUE")
print("=" * 70)

data = orders[
    [
        "order_value",
        "freight_ratio"
    ]
].dropna()

pearson_r, pearson_p = stats.pearsonr(
    data["order_value"],
    data["freight_ratio"]
)

print(f"Sample size         : {len(data):,}")
print(f"Pearson correlation : {pearson_r:.4f}")
print(f"p-value             : {pearson_p:.6f}")

results.append({
    "analysis": "Freight Ratio vs Order Value",
    "test": "Pearson correlation",
    "sample_size": len(data),
    "statistic": pearson_r,
    "p_value": pearson_p,
    "effect_size": pearson_r,
    "interpretation": (
        "Negative association between order value "
        "and freight ratio"
    )
})


# ============================================================
# 5. LATE VS ON-TIME REVIEW SCORES
# ============================================================

print("\n" + "=" * 70)
print("5. LATE VS ON-TIME REVIEW SCORES")
print("=" * 70)

data = orders[
    (orders["is_delivered"] == 1)
    & orders["review_score"].notna()
].copy()

late_reviews = data.loc[
    data["is_late"] == 1,
    "review_score"
].dropna()

on_time_reviews = data.loc[
    data["is_late"] == 0,
    "review_score"
].dropna()

late_mean = late_reviews.mean()

on_time_mean = on_time_reviews.mean()

mean_difference = (
    late_mean - on_time_mean
)

t_stat, t_p = stats.ttest_ind(
    late_reviews,
    on_time_reviews,
    equal_var=False
)

u_stat, u_p = stats.mannwhitneyu(
    late_reviews,
    on_time_reviews,
    alternative="two-sided"
)

late_ci = confidence_interval_mean(
    late_reviews
)

on_time_ci = confidence_interval_mean(
    on_time_reviews
)

print(f"Late orders sample       : {len(late_reviews):,}")
print(f"On-time orders sample    : {len(on_time_reviews):,}")

print(f"\nLate mean review         : {late_mean:.4f}")
print(f"On-time mean review      : {on_time_mean:.4f}")
print(f"Mean difference          : {mean_difference:.4f}")

print(f"\nWelch t-statistic        : {t_stat:.4f}")
print(f"Welch p-value            : {t_p:.6f}")

print(f"\nMann-Whitney U statistic : {u_stat:.4f}")
print(f"Mann-Whitney p-value     : {u_p:.6f}")

print(
    f"\nLate review 95% CI       : "
    f"({late_ci[0]:.4f}, {late_ci[1]:.4f})"
)

print(
    f"On-time review 95% CI    : "
    f"({on_time_ci[0]:.4f}, {on_time_ci[1]:.4f})"
)

results.append({
    "analysis": "Late vs On-Time Review Scores",
    "test": "Welch t-test",
    "sample_size": (
        len(late_reviews)
        + len(on_time_reviews)
    ),
    "statistic": t_stat,
    "p_value": t_p,
    "effect_size": mean_difference,
    "interpretation": (
        "Compares mean review scores between "
        "late and on-time deliveries"
    )
})


# ============================================================
# 6. LOW SATISFACTION RATE: LATE VS ON-TIME
# ============================================================

print("\n" + "=" * 70)
print("6. LOW SATISFACTION RATE: LATE VS ON-TIME")
print("=" * 70)

data = orders[
    (orders["is_delivered"] == 1)
    & orders["low_satisfaction"].notna()
].copy()

late_low = data.loc[
    data["is_late"] == 1,
    "low_satisfaction"
].sum()

late_total = data.loc[
    data["is_late"] == 1
].shape[0]

on_time_low = data.loc[
    data["is_late"] == 0,
    "low_satisfaction"
].sum()

on_time_total = data.loc[
    data["is_late"] == 0
].shape[0]

late_low_rate = (
    late_low
    / late_total
    * 100
)

on_time_low_rate = (
    on_time_low
    / on_time_total
    * 100
)

contingency_table = np.array([
    [
        late_low,
        late_total - late_low
    ],
    [
        on_time_low,
        on_time_total - on_time_low
    ]
])

chi2, chi_p, dof, expected = stats.chi2_contingency(
    contingency_table
)

print(f"Late low satisfaction       : {late_low:,}")
print(f"Late total                  : {late_total:,}")
print(f"Late low satisfaction rate  : {late_low_rate:.2f}%")

print(f"\nOn-time low satisfaction    : {on_time_low:,}")
print(f"On-time total               : {on_time_total:,}")
print(
    f"On-time low satisfaction rate: "
    f"{on_time_low_rate:.2f}%"
)

print(f"\nChi-square statistic        : {chi2:.4f}")
print(f"Chi-square p-value          : {chi_p:.6f}")

results.append({
    "analysis": "Late vs On-Time Low Satisfaction",
    "test": "Chi-square test",
    "sample_size": len(data),
    "statistic": chi2,
    "p_value": chi_p,
    "effect_size": (
        late_low_rate
        - on_time_low_rate
    ),
    "interpretation": (
        "Compares low-satisfaction proportions "
        "between late and on-time deliveries"
    )
})


# ============================================================
# 7. DELIVERY TIME CONFIDENCE INTERVAL
# ============================================================

print("\n" + "=" * 70)
print("7. DELIVERY TIME CONFIDENCE INTERVAL")
print("=" * 70)

delivery_days = orders.loc[
    orders["is_delivered"] == 1,
    "delivery_days"
].dropna()

delivery_mean = delivery_days.mean()

delivery_ci = confidence_interval_mean(
    delivery_days
)

print(f"Sample size      : {len(delivery_days):,}")
print(f"Mean delivery    : {delivery_mean:.4f} days")

print(
    f"95% CI           : "
    f"({delivery_ci[0]:.4f}, {delivery_ci[1]:.4f})"
)

results.append({
    "analysis": "Average Delivery Time",
    "test": "95% Confidence Interval",
    "sample_size": len(delivery_days),
    "statistic": delivery_mean,
    "p_value": np.nan,
    "effect_size": np.nan,
    "interpretation": (
        "Confidence interval for the mean delivery time"
    )
})


# ============================================================
# 8. REVIEW SCORE CONFIDENCE INTERVAL
# ============================================================

print("\n" + "=" * 70)
print("8. REVIEW SCORE CONFIDENCE INTERVAL")
print("=" * 70)

review_scores = orders[
    "review_score"
].dropna()

review_mean = review_scores.mean()

review_ci = confidence_interval_mean(
    review_scores
)

print(f"Sample size      : {len(review_scores):,}")
print(f"Mean review      : {review_mean:.4f}")

print(
    f"95% CI           : "
    f"({review_ci[0]:.4f}, {review_ci[1]:.4f})"
)

results.append({
    "analysis": "Average Review Score",
    "test": "95% Confidence Interval",
    "sample_size": len(review_scores),
    "statistic": review_mean,
    "p_value": np.nan,
    "effect_size": np.nan,
    "interpretation": (
        "Confidence interval for the mean review score"
    )
})


# ============================================================
# 9. STATE-LEVEL DELIVERY VS REVIEW RELATIONSHIP
# ============================================================

print("\n" + "=" * 70)
print("9. STATE-LEVEL DELIVERY VS REVIEW RELATIONSHIP")
print("=" * 70)

state_data = (
    orders[
        orders["is_delivered"] == 1
    ]
    .groupby("customer_state")
    .agg(
        avg_delivery_days=(
            "delivery_days",
            "mean"
        ),
        avg_review=(
            "review_score",
            "mean"
        ),
        orders=(
            "order_id",
            "nunique"
        )
    )
    .reset_index()
)

state_data = state_data[
    state_data["orders"] >= 50
].dropna(
    subset=[
        "avg_delivery_days",
        "avg_review"
    ]
)

state_r, state_p = stats.pearsonr(
    state_data["avg_delivery_days"],
    state_data["avg_review"]
)

print(
    f"States included       : {len(state_data)}"
)

print(
    f"Pearson correlation    : {state_r:.4f}"
)

print(
    f"p-value               : {state_p:.6f}"
)

results.append({
    "analysis": "State Avg Delivery Days vs Avg Review",
    "test": "Pearson correlation",
    "sample_size": len(state_data),
    "statistic": state_r,
    "p_value": state_p,
    "effect_size": state_r,
    "interpretation": (
        "State-level association between average "
        "delivery time and average review score"
    )
})


# ============================================================
# 10. SUMMARY TABLE
# ============================================================

print("\n" + "=" * 70)
print("10. STATISTICAL TEST SUMMARY")
print("=" * 70)

results_df = pd.DataFrame(results)

print(
    results_df.to_string(
        index=False
    )
)


# ============================================================
# SIGNIFICANCE FLAG
# ============================================================

results_df["statistically_significant"] = (
    results_df["p_value"] < 0.05
)

results_df.to_csv(
    EDA_DIR / "statistical_tests.csv",
    index=False
)


# ============================================================
# KEY NUMERIC SUMMARY
# ============================================================

summary = pd.DataFrame([
    {
        "metric": "Average Delivery Days",
        "value": delivery_mean,
        "ci_lower": delivery_ci[0],
        "ci_upper": delivery_ci[1]
    },
    {
        "metric": "Average Review Score",
        "value": review_mean,
        "ci_lower": review_ci[0],
        "ci_upper": review_ci[1]
    },
    {
        "metric": "Late Delivery Review Difference",
        "value": mean_difference,
        "ci_lower": np.nan,
        "ci_upper": np.nan
    },
    {
        "metric": "Late Low Satisfaction Rate",
        "value": late_low_rate,
        "ci_lower": np.nan,
        "ci_upper": np.nan
    },
    {
        "metric": "On-Time Low Satisfaction Rate",
        "value": on_time_low_rate,
        "ci_lower": np.nan,
        "ci_upper": np.nan
    }
])

summary.to_csv(
    EDA_DIR / "statistical_summary.csv",
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("STATISTICAL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated:")
print(
    EDA_DIR / "statistical_tests.csv"
)

print(
    EDA_DIR / "statistical_summary.csv"
)

print("\nNext stage:")
print("Churn-driver analysis / predictive modeling")