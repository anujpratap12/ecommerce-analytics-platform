# UAT Test Cases & Validation

## 1. Purpose

This document defines user acceptance test scenarios for validating whether the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform satisfies its documented business and functional requirements.

The test cases focus on business KPIs, dashboard functionality, analytical outputs, data quality, and business rules.

> Note: These are project-level UAT scenarios. They do not represent formal sign-off from real organizational business users.

---

# 2. UAT Scope

The following areas are covered:

- Executive KPIs
- Customer retention
- RFM segmentation
- Churn-risk analysis
- Fulfillment performance
- Customer satisfaction
- Product performance
- Freight analysis
- Regional analysis
- Dashboard filtering
- Data validation
- Business rules

---

# 3. UAT Test Cases

| Test ID | Requirement | Test Scenario | Expected Result | Status |
|---|---|---|---|---|
| UAT-01 | FR-05 | Verify Total Orders KPI | Dashboard displays the validated order count | Pass |
| UAT-02 | FR-05 | Verify Total Revenue KPI | Dashboard displays revenue from the analytical dataset | Pass |
| UAT-03 | FR-05 | Verify Total Customers KPI | Dashboard displays distinct observed customers | Pass |
| UAT-04 | FR-05 | Verify Average Review Score | Dashboard displays the calculated average review score | Pass |
| UAT-05 | FR-05 | Verify Late Delivery Rate | Dashboard displays late delivered orders as a percentage of delivered orders | Pass |
| UAT-06 | FR-06 | Verify Repeat Customer analysis | Repeat customer count and rate are available | Pass |
| UAT-07 | FR-07 | Verify RFM segmentation | Customers are assigned to documented RFM segments | Pass |
| UAT-08 | FR-08 | Verify churn-risk analysis | Customer churn-risk probabilities and segments are available | Pass |
| UAT-09 | FR-09 | Verify fulfillment metrics | Delivery days, freight, late delivery and risk metrics are available | Pass |
| UAT-10 | FR-10 | Verify regional fulfillment analysis | State-level late delivery analysis is available | Pass |
| UAT-11 | FR-11 | Verify satisfaction analysis | Review score and low-satisfaction analysis are available | Pass |
| UAT-12 | FR-12 | Verify product analysis | Category revenue and product performance metrics are available | Pass |
| UAT-13 | FR-13 | Verify root cause analysis | Delivery, fulfillment and satisfaction relationships can be investigated | Pass |
| UAT-14 | FR-15 | Verify dashboard filtering | Available filters update relevant visuals consistently | Pass |
| UAT-15 | FR-16 | Verify KPI definitions | Dashboard calculations follow documented KPI definitions | Pass |
| UAT-16 | FR-17 | Verify data validation | Data-quality checks and analytical validations are available | Pass |

---

# 4. Detailed UAT Scenarios

## UAT-01 — Executive KPI Validation

### Objective

Verify that the Executive Overview provides the required business KPIs.

### Steps

1. Open the Executive Overview dashboard.
2. Review the KPI cards.
3. Compare the displayed values with validated analytical outputs.

### Expected Result

Required executive KPIs are displayed and use the documented definitions.

### Status

**Pass**

---

## UAT-02 — Customer Retention Validation

### Objective

Verify customer retention analysis.

### Steps

1. Open the Customer Retention dashboard.
2. Review Repeat Customers.
3. Review Repeat Customer Rate.
4. Review purchase frequency.
5. Review RFM segmentation.

### Expected Result

Customer retention metrics and segments are available and respond correctly to applicable filters.

### Status

**Pass**

---

## UAT-03 — Fulfillment Validation

### Objective

Verify fulfillment and logistics analysis.

### Steps

1. Open the Fulfillment & Logistics dashboard.
2. Review Late Delivery Rate.
3. Review Average Delivery Days.
4. Review Average Freight Cost.
5. Review fulfillment-risk analysis.
6. Compare late and on-time orders.

### Expected Result

Fulfillment KPIs and analytical comparisons are available.

### Status

**Pass**

---

## UAT-04 — Customer Experience Validation

### Objective

Verify customer satisfaction analysis.

### Steps

1. Open the Customer Experience dashboard.
2. Review Average Review Score.
3. Review review score distribution.
4. Review low satisfaction analysis.
5. Compare late and on-time delivery satisfaction.

### Expected Result

Customer satisfaction metrics and comparisons are displayed correctly.

### Status

**Pass**

---

## UAT-05 — Product and Profitability Validation

### Objective

Verify product and order-economics analysis.

### Steps

1. Open the Profitability & Product Performance dashboard.
2. Review revenue by category.
3. Review freight ratio.
4. Review contribution proxy.
5. Review product price and freight relationships.

### Expected Result

Product and profitability-related analytical metrics are available.

### Status

**Pass**

---

## UAT-06 — Root Cause Analysis Validation

### Objective

Verify that the Root Cause Analysis dashboard supports operational investigation.

### Steps

1. Open the Root Cause Analysis dashboard.
2. Review state-level late delivery rates.
3. Review satisfaction across fulfillment-risk segments.
4. Compare late and on-time review scores.

### Expected Result

The dashboard provides analytical evidence that can be used to investigate operational and customer-experience issues.

### Status

**Pass**

---

# 5. Data Validation / SIT Evidence

The project also includes technical validation performed during the data and analytical pipeline.

Validated areas include:

- Missing values.
- Duplicate records.
- Negative price/freight values.
- Invalid dates.
- Referential integrity.
- Duplicate order IDs.
- Duplicate customer IDs.
- Order status distribution.
- Review score distribution.
- SQL KPI validation.
- Python analytical validation.
- Automated Python tests.

Existing automated tests include:

```text
pytest tests/test_validation.py
pytest tests/test_rules.py