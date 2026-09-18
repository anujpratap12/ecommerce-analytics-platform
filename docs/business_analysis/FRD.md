# Functional Requirements Document (FRD)

## 1. Document Purpose

This document defines the functional and non-functional requirements for the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform.

The FRD translates the business requirements defined in the BRD into specific analytical, data-processing, reporting, and dashboard functionality.

---

## 2. Solution Scope

The solution will:

- Process historical e-commerce data.
- Perform data cleaning and validation.
- Store analytical data in PostgreSQL.
- Perform SQL-based business analysis.
- Perform Python-based exploratory and statistical analysis.
- Segment customers using RFM analysis.
- Classify customer churn risk.
- Analyze fulfillment and delivery performance.
- Analyze customer satisfaction.
- Analyze product and category performance.
- Provide interactive Power BI dashboards.
- Provide business insights and recommendations.

---

# 3. Functional Requirements

## FR-01 — Data Ingestion

The system shall ingest the available e-commerce datasets including:

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

### Expected Output

Clean and accessible datasets for downstream analytical processing.

---

## FR-02 — Data Cleaning

The system shall:

- Standardize column formats.
- Parse date and timestamp fields.
- Normalize categorical values.
- Handle missing values according to business/data-quality rules.
- Remove exact duplicate records where applicable.
- Validate numeric fields.
- Standardize customer, seller, city, and state information.

### Expected Output

Cleaned analytical datasets suitable for analysis.

---

## FR-03 — Data Quality Validation

The system shall validate:

- Missing values.
- Duplicate records.
- Invalid numeric values.
- Invalid dates.
- Referential integrity.
- Duplicate business keys.
- Unexpected categorical values.

### Expected Output

A data-quality report documenting validation results.

---

## FR-04 — Analytical Data Storage

The system shall store processed data in PostgreSQL.

The database shall support:

- Staging data.
- Analytical datasets.
- SQL-based business analysis.
- Reporting and dashboard consumption.

### Expected Output

Validated analytical tables available for querying.

---

## FR-05 — Executive KPI Analysis

The system shall calculate:

- Total Orders
- Total Customers
- Total Revenue
- Total Freight Cost
- Average Order Value
- Average Review Score
- Late Delivery Rate
- Average Delivery Days
- Repeat Customer Rate
- Contribution Proxy

### Expected Output

Standardized executive KPIs available for reporting.

---

## FR-06 — Customer Retention Analysis

The system shall analyze customer purchasing behavior using:

- Customer order frequency.
- Customer recency.
- Customer monetary value.
- Customer lifetime orders.
- Repeat customer identification.
- Customer value segmentation.

### Expected Output

Customer retention and purchasing behavior analysis.

---

## FR-07 — RFM Segmentation

The system shall segment customers using:

- Recency
- Frequency
- Monetary Value

The solution shall identify relevant customer segments such as:

- High Value Active
- Loyal
- Active
- At Risk
- At Risk - High Value
- Inactive

### Expected Output

Customer segments available for retention analysis and visualization.

---

## FR-08 — Churn-Risk Analysis

The system shall:

- Define an analytical churn criterion based on customer recency.
- Generate customer-level analytical features.
- Train a churn-risk classification model.
- Generate churn-risk probabilities.
- Segment customers into risk groups.

### Expected Output

Customer churn-risk analysis and risk segmentation.

### Analytical Limitation

The churn label is analytically derived from customer recency and is not a directly observed business churn flag.

The current model uses customer-level historical features. Therefore, the model should be interpreted as a portfolio analytical classification exercise rather than a production-ready predictive churn system.

---

## FR-09 — Fulfillment Analysis

The system shall calculate and analyze:

- Delivery days.
- Delivery delay.
- Late delivery status.
- Late delivery rate.
- Freight cost.
- Freight ratio.
- Fulfillment risk.

### Expected Output

Fulfillment performance metrics for operational analysis.

---

## FR-10 — Regional Fulfillment Analysis

The system shall compare fulfillment performance across customer states.

The analysis shall include:

- Late delivery rate by state.
- Delivery performance by state.
- Regional order performance.
- Regional freight metrics where applicable.

### Expected Output

Identification of regions requiring operational investigation.

---

## FR-11 — Customer Satisfaction Analysis

The system shall analyze:

- Average review score.
- Review score distribution.
- Low-satisfaction customers.
- Satisfaction by delivery status.
- Satisfaction across fulfillment-risk segments.

### Expected Output

Customer experience and satisfaction analysis.

---

## FR-12 — Product Performance Analysis

The system shall analyze:

- Product category revenue.
- Product prices.
- Freight costs.
- Freight ratio.
- Product/category contribution proxy.
- Top-performing product categories.

### Expected Output

Product and category performance analysis.

---

## FR-13 — Root Cause Analysis

The system shall support investigation of relationships between:

- Delivery performance and customer satisfaction.
- Fulfillment risk and satisfaction.
- Freight cost and order value.
- Regional performance and delivery delays.
- Customer behavior and retention risk.

### Expected Output

Evidence-based analytical findings that help identify areas requiring business investigation.

---

## FR-14 — Power BI Dashboard

The solution shall provide six analytical dashboard views:

### Executive Overview

Provides overall business KPIs and trends.

### Customer Retention

Provides customer behavior, RFM segmentation, purchase frequency, and churn-risk analysis.

### Fulfillment & Logistics

Provides delivery, freight, fulfillment-risk, and regional performance analysis.

### Customer Experience

Provides review distribution, satisfaction analysis, and satisfaction trends.

### Profitability & Product Performance

Provides revenue, freight, contribution proxy, and product/category analysis.

### Root Cause Analysis

Provides operational and customer-experience relationships requiring investigation.

---

## FR-15 — Interactive Filtering

The dashboard shall allow users to interact with analytical views using available filters.

Filtering shall update relevant KPIs and visualizations consistently.

---

## FR-16 — KPI Consistency

The solution shall ensure that KPIs displayed in dashboards are based on documented definitions and validated analytical data.

Metric definitions shall remain consistent across:

- Python analysis.
- SQL analysis.
- Power BI.

---

## FR-17 — Data Validation and Testing

The solution shall include validation and testing of:

- Data quality.
- SQL analytical outputs.
- Python analytical processing.
- Business rules.
- Dashboard calculations.
- User acceptance scenarios.

### Expected Output

Documented validation and testing results.

---

# 4. Non-Functional Requirements

## NFR-01 — Data Accuracy

Analytical outputs should be based on validated and cleaned source data.

## NFR-02 — Data Consistency

Business metrics should use consistent definitions across analytical layers.

## NFR-03 — Usability

Dashboards should present KPIs and analytical findings in a clear and understandable format for business users.

## NFR-04 — Maintainability

ETL, SQL, Python, and analytical logic should be organized into separate project components.

## NFR-05 — Reproducibility

The analytical pipeline should be reproducible using the documented project structure, dependencies, and processing scripts.

## NFR-06 — Performance

SQL queries and Power BI reports should be designed to support efficient analytical exploration of the available dataset.

## NFR-07 — Documentation

Business requirements, functional requirements, analytical definitions, validation procedures, and project limitations shall be documented.

## NFR-08 — Security

Sensitive credentials and environment variables shall not be stored in the public repository.

---

# 5. Business Rules

## BRULE-01 — Late Delivery

An order is considered late when the actual customer delivery date occurs after the estimated delivery date.

## BRULE-02 — Low Satisfaction

A review score of 1 or 2 is classified as low satisfaction.

## BRULE-03 — Repeat Customer

A customer is considered a repeat customer when the customer has placed more than one order.

## BRULE-04 — Analytical Churn

A customer is classified as analytically churned when their recency exceeds the defined 180-day threshold.

## BRULE-05 — Contribution Proxy

Contribution Proxy is calculated as order/product revenue less freight cost.

This metric is a profitability-related analytical proxy and should not be interpreted as accounting profit.

---

# 6. Reporting Requirements

The reporting solution shall provide:

- Executive KPI monitoring.
- Monthly trend analysis.
- Customer segmentation.
- Fulfillment performance monitoring.
- Regional comparisons.
- Customer satisfaction analysis.
- Product/category performance.
- Root-cause-oriented analysis.

---

# 7. Expected Outputs

The final solution shall produce:

1. Cleaned analytical datasets.
2. Data-quality reports.
3. PostgreSQL analytical tables.
4. SQL business analysis.
5. Python EDA and statistical analysis.
6. Customer RFM segmentation.
7. Churn-risk classification.
8. Power BI dashboards.
9. Business insights.
10. Business recommendations.
11. Validation and testing documentation.

---

# 8. Acceptance Summary

The solution will satisfy the functional requirements when:

- Data can be processed through the defined ETL workflow.
- Data-quality checks are successfully executed.
- Analytical data is available in PostgreSQL.
- Required KPIs can be calculated.
- Customer retention analysis is available.
- Fulfillment analysis is available.
- Customer satisfaction analysis is available.
- Product/category analysis is available.
- Churn-risk analysis is available.
- Power BI dashboards display the required analytical views.
- Dashboard calculations are validated.
- Business requirements can be traced to analytical outputs and test scenarios.