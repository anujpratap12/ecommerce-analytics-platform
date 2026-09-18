# Process & Gap Analysis

## 1. Purpose

This document describes the high-level e-commerce order and customer experience process and identifies analytical gaps that can be addressed through the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform.

---

# 2. High-Level Business Process

The simplified e-commerce process is:

Customer Places Order
↓
Order Processing
↓
Seller Fulfillment
↓
Order Shipment
↓
Customer Delivery
↓
Customer Review
↓
Customer Future Purchase / Retention

Each stage produces data that can be analyzed to identify performance patterns.

---

# 3. AS-IS Process

## Customer Order

The customer places an order through the e-commerce platform.

Available analytical information includes:

- Customer
- Order
- Order items
- Payment
- Product
- Seller

↓

## Fulfillment

The order is processed and fulfilled by the seller.

Relevant analytical information includes:

- Order status
- Seller
- Product
- Order item value
- Freight cost

↓

## Delivery

The order is shipped and delivered to the customer.

Relevant metrics include:

- Delivery date
- Estimated delivery date
- Delivery days
- Delivery delay
- Late delivery status

↓

## Customer Experience

The customer provides a review after the order.

Relevant information includes:

- Review score
- Review title
- Review message
- Delivery performance

↓

## Customer Retention

The customer may place additional orders.

Relevant metrics include:

- Number of orders
- Recency
- Frequency
- Monetary value
- Repeat customer status
- Churn-risk classification

---

# 4. Identified Business Gaps

| Gap ID | Business Gap | Impact | Analytical Response |
|---|---|---|---|
| GAP-01 | Limited visibility into overall business KPIs | Difficult to monitor performance | Executive dashboard |
| GAP-02 | Limited visibility into regional delivery performance | Difficult to identify operational problem areas | State-level fulfillment analysis |
| GAP-03 | Delivery delays may affect customer experience | Potential dissatisfaction | Delivery vs satisfaction analysis |
| GAP-04 | Customer purchasing behavior is not segmented | Difficult to identify customer groups | RFM segmentation |
| GAP-05 | Customer churn risk is not directly visible | Retention opportunities may be missed | Churn-risk classification |
| GAP-06 | Freight cost impact is not easily monitored | Difficulty evaluating order economics | Freight and contribution analysis |
| GAP-07 | Product/category performance requires comparison | Difficult to prioritize categories | Product/category analytics |
| GAP-08 | Analytical metrics may be inconsistent without standard definitions | Reporting reliability risk | Documented KPI definitions and validation |

---

# 5. TO-BE Analytical Process

The proposed analytical process is:

Business Requirements
↓
Data Collection
↓
Data Quality Validation
↓
Python ETL
↓
PostgreSQL Analytical Storage
↓
SQL Business Analysis
↓
Python EDA & Statistical Analysis
↓
Customer RFM & Churn-Risk Analysis
↓
Power BI Reporting
↓
Root Cause Analysis
↓
Business Insights
↓
Recommendations

---

# 6. Gap-to-Solution Mapping

| Gap | Proposed Solution | Expected Outcome |
|---|---|---|
| KPI visibility | Executive Dashboard | Centralized performance monitoring |
| Regional delivery issues | Fulfillment Dashboard | Regional comparison |
| Customer dissatisfaction | Customer Experience Analysis | Identify satisfaction patterns |
| Limited retention visibility | RFM Analysis | Customer segmentation |
| Churn-risk visibility | Churn Model | Risk-based customer analysis |
| Freight cost visibility | Profitability Analysis | Better order-economics visibility |
| Product comparison | Product Analytics | Category performance comparison |
| Metric inconsistency | KPI definitions + validation | Consistent reporting |

---

# 7. Root Cause Analysis Framework

The platform uses an analytical investigation approach:

### Problem

Identify a business KPI or performance issue.

↓

### Segmentation

Break the problem down by:

- State
- Customer segment
- Fulfillment risk
- Product category
- Time period

↓

### Comparison

Compare relevant groups.

Examples:

- Late vs On-Time
- High Risk vs Normal Risk
- Repeat vs One-Time Customers
- High vs Low Freight Ratio

↓

### Statistical Analysis

Where appropriate, evaluate relationships using:

- Correlation analysis
- Hypothesis testing
- Confidence intervals

↓

### Business Interpretation

Translate analytical findings into areas requiring operational investigation.

---

# 8. Current-State vs Future-State Capability

| Capability | Current State | Future Analytical State |
|---|---|---|
| KPI monitoring | Distributed analysis | Centralized dashboard |
| Fulfillment monitoring | Historical data | Regional KPI monitoring |
| Customer analysis | Transaction-level data | RFM and churn-risk segmentation |
| Satisfaction analysis | Review records | Delivery and satisfaction analysis |
| Product analysis | Product transactions | Category performance analysis |
| Cost analysis | Freight transaction data | Freight ratio and contribution proxy |
| Validation | Raw analytical outputs | Documented data and KPI validation |

---

# 9. Business Impact Areas

The analytical platform supports investigation of:

- Delivery performance
- Customer satisfaction
- Customer retention
- Churn risk
- Freight cost
- Product performance
- Regional performance
- Order economics

The analysis does not claim that observed relationships are causal. Findings should be treated as evidence for further business investigation.

---

# 10. Process Limitations

The available dataset does not provide:

- Explicit carrier information.
- Warehouse identifiers.
- Marketing campaign information.
- Customer acquisition cost.
- Complete accounting cost information.

Therefore, process analysis is limited to the operational and customer information represented in the dataset.