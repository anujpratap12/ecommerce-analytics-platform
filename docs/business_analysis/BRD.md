# Business Requirements Document (BRD)

## 1. Project Overview

### Project Name
E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform

### Business Context

The e-commerce business needs better visibility into customer retention, fulfillment performance, customer satisfaction, product performance, and profitability-related metrics.

The analytics platform uses historical e-commerce transaction data to identify operational and customer-related patterns and provide business stakeholders with data-driven insights for decision-making.

### Business Problem

The business needs to understand:

- Which regions experience higher delivery delays.
- How fulfillment performance relates to customer satisfaction.
- Which customers or customer segments show retention or churn risk.
- Which product categories generate higher revenue.
- Where freight costs create pressure on order economics.
- Which operational areas require further investigation.

---

## 2. Business Objectives

The primary objectives are:

1. Monitor overall e-commerce business performance using standardized KPIs.
2. Analyze customer purchase behavior and retention patterns.
3. Identify customer segments based on recency, frequency, and monetary value.
4. Identify customers with higher churn risk using analytical modeling.
5. Analyze fulfillment and delivery performance across regions.
6. Understand the relationship between delivery performance and customer satisfaction.
7. Analyze revenue, freight costs, and contribution proxy across products and categories.
8. Identify regional and operational areas requiring further investigation.
9. Provide interactive dashboards for business decision support.
10. Support data-driven recommendations for improving customer experience and operational performance.

---

## 3. Stakeholders

| Stakeholder | Primary Information Need |
|---|---|
| Business Manager | Overall business performance and key KPIs |
| Operations Manager | Delivery and fulfillment performance |
| Customer Experience Manager | Customer satisfaction and review trends |
| CRM / Customer Analytics Team | Customer retention and churn-risk segments |
| Finance / Commercial Team | Revenue, freight cost and contribution analysis |
| Product / Category Manager | Product and category performance |
| Data / BI Analyst | Data quality, analytical models and reporting |

---

## 4. Business Questions

The platform should help answer the following questions:

### Customer Retention

- What percentage of customers are repeat customers?
- How frequently do customers purchase?
- Which customer segments have higher retention or churn risk?
- Which customer groups have higher customer value?

### Fulfillment & Logistics

- What is the overall late delivery rate?
- Which states have higher late delivery rates?
- What is the average delivery time?
- Which fulfillment risk segments require attention?
- How does freight cost vary across orders and regions?

### Customer Experience

- What is the average review score?
- How does late delivery relate to customer satisfaction?
- What percentage of late-delivery customers provide low satisfaction scores?
- How does satisfaction change across fulfillment-risk segments?

### Profitability & Product Performance

- Which product categories generate the highest revenue?
- How does freight cost vary with order value?
- Which categories have higher contribution proxy?
- Where does freight represent a larger proportion of order value?

---

## 5. Key Performance Indicators (KPIs)

| KPI | Business Purpose |
|---|---|
| Total Orders | Measure order volume |
| Total Customers | Measure customer base |
| Total Revenue | Measure product revenue |
| Total Freight Cost | Monitor shipping-related costs |
| Average Order Value | Monitor average revenue per order |
| Average Review Score | Monitor customer satisfaction |
| Late Delivery Rate | Monitor fulfillment performance |
| Average Delivery Days | Monitor delivery efficiency |
| Repeat Customer Rate | Monitor customer retention |
| Churn Rate | Monitor customer attrition |
| Contribution Proxy | Monitor order economics using revenue less freight cost |
| Low Satisfaction Rate | Monitor customer dissatisfaction |

> **Note:** Contribution Proxy is an analytical metric defined as order value/revenue less freight cost. It is not equivalent to accounting profit because the dataset does not contain complete product acquisition costs, operating expenses, taxes, or other cost components.

---

## 6. Data Sources

The primary data source is the Olist Brazilian E-Commerce Public Dataset.

The dataset contains information related to:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translation

The project does not contain explicit carrier names, warehouse identifiers, marketing campaign data, customer acquisition costs, or complete accounting profit information.

---

## 7. High-Level Solution

The proposed analytics solution follows the flow:

Raw E-Commerce Data
↓
Python Data Cleaning & ETL
↓
Data Quality Validation
↓
PostgreSQL
↓
SQL Analytics
↓
Python EDA & Statistical Analysis
↓
Customer RFM & Churn-Risk Analysis
↓
Power BI Data Model
↓
Interactive Business Dashboards
↓
Business Insights & Recommendations

---

## 8. Dashboard Requirements

The Power BI solution should provide the following analytical views:

### Dashboard 1 — Executive Overview

Provide:

- Total Orders
- Total Revenue
- Total Customers
- Total Freight Cost
- Average Review Score
- Late Delivery Rate
- Average Order Value
- Monthly business trends
- Regional revenue performance

### Dashboard 2 — Customer Retention

Provide:

- Repeat Customers
- Repeat Customer Rate
- Purchase frequency
- RFM segmentation
- Churn-risk analysis
- Customer distribution by state

### Dashboard 3 — Fulfillment & Logistics

Provide:

- Late Delivery Rate
- Average Delivery Days
- Average Freight Cost
- Fulfillment Risk
- Late vs On-Time Orders
- Late Delivery Rate by State
- Delivery performance trends
- Satisfaction comparison by delivery status

### Dashboard 4 — Customer Experience

Provide:

- Average Review Score
- Review Score Distribution
- Low Satisfaction comparison
- Satisfaction trend
- Delivery and satisfaction relationship

### Dashboard 5 — Profitability & Product Performance

Provide:

- Contribution Proxy
- Average Freight Ratio
- Product/category revenue
- Product contribution analysis
- Product pricing analysis
- Freight vs product price relationship
- Top product categories

### Dashboard 6 — Root Cause Analysis

Provide:

- States with higher late delivery rates
- Low satisfaction across fulfillment-risk segments
- Late vs on-time satisfaction comparison
- Supporting operational analysis

---

## 9. Business Requirements

| ID | Requirement | Priority |
|---|---|---|
| BR-01 | Provide an executive view of business KPIs | High |
| BR-02 | Analyze customer retention and purchasing behavior | High |
| BR-03 | Segment customers using RFM analysis | High |
| BR-04 | Identify customer churn-risk patterns | High |
| BR-05 | Monitor delivery and fulfillment performance | High |
| BR-06 | Compare fulfillment performance across states | High |
| BR-07 | Analyze customer satisfaction and reviews | High |
| BR-08 | Analyze revenue and freight cost | High |
| BR-09 | Analyze product/category performance | Medium |
| BR-10 | Provide root-cause-oriented operational analysis | High |
| BR-11 | Enable interactive filtering and dashboard exploration | High |
| BR-12 | Provide validated and consistent analytical metrics | High |

---

## 10. Business Constraints

The analysis is subject to the limitations of the available dataset.

Key constraints include:

- Historical data represents the available observation period rather than current business operations.
- Explicit carrier information is unavailable.
- Warehouse information is unavailable.
- Marketing campaign information is unavailable.
- Complete product cost information is unavailable.
- True accounting profit cannot be calculated from the available data.
- Churn is an analytical definition based on customer recency rather than a directly observed business churn flag.

---

## 11. Expected Business Outcomes

The platform is expected to help stakeholders:

- Identify fulfillment problem areas.
- Understand customer satisfaction patterns.
- Identify customer segments requiring retention attention.
- Monitor revenue and freight-related metrics.
- Compare regional performance.
- Investigate operational root causes.
- Make data-driven decisions using standardized KPIs and interactive dashboards.

---

## 12. Success Criteria

The project will be considered successful when:

- Required datasets are cleaned and validated.
- Analytical data is available in PostgreSQL.
- Business KPIs can be calculated consistently.
- Customer retention and churn-risk analysis is available.
- Fulfillment and satisfaction analysis is available.
- Product and revenue analysis is available.
- Power BI dashboards provide the required business views.
- Analytical outputs are validated through SQL/Python testing.
- Business insights and recommendations can be derived from the results.