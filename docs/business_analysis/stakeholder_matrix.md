# Stakeholder Matrix

## 1. Purpose

This document identifies the key stakeholder groups relevant to the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform and maps their information needs to the analytical solution.

> Note: These stakeholder personas represent the business users the solution is designed to support. They are not claims of actual stakeholder interviews or organizational roles held during the project.

---

## 2. Stakeholder Overview

| Stakeholder | Primary Objective | Key Information Required | Relevant Dashboard |
|---|---|---|---|
| Business Manager | Monitor overall business performance | Orders, revenue, customers, AOV, satisfaction, delivery KPIs | Executive Overview |
| Operations Manager | Monitor fulfillment performance | Delivery days, late rate, freight, regional performance | Fulfillment & Logistics |
| Customer Experience Manager | Improve customer experience | Review scores, low satisfaction, delivery-related dissatisfaction | Customer Experience |
| CRM / Customer Analytics Team | Understand retention | Repeat customers, RFM segments, churn-risk | Customer Retention |
| Finance / Commercial Team | Monitor order economics | Revenue, freight cost, contribution proxy | Profitability & Product Performance |
| Product / Category Manager | Evaluate product performance | Category revenue, price, freight, contribution proxy | Profitability & Product Performance |
| Data / BI Analyst | Maintain analytical reporting | Data quality, SQL outputs, KPIs, dashboard calculations | All Dashboards |

---

## 3. Stakeholder Needs

### Business Manager

Needs a consolidated view of business performance to identify major trends and areas requiring attention.

Key KPIs:

- Total Orders
- Total Revenue
- Total Customers
- Average Order Value
- Average Review Score
- Late Delivery Rate

---

### Operations Manager

Needs visibility into fulfillment and regional delivery performance.

Key metrics:

- Average Delivery Days
- Late Delivery Rate
- Delivery Delay
- Freight Cost
- Fulfillment Risk
- Late Delivery Rate by State

---

### Customer Experience Manager

Needs to understand customer satisfaction and potential relationships between delivery performance and reviews.

Key metrics:

- Average Review Score
- Review Score Distribution
- Low Satisfaction Rate
- Satisfaction by Delivery Status
- Satisfaction by Fulfillment Risk

---

### CRM / Customer Analytics Team

Needs customer-level and segment-level insights for retention analysis.

Key metrics:

- Repeat Customer Rate
- Purchase Frequency
- Recency
- Frequency
- Monetary Value
- RFM Segment
- Churn Risk

---

### Finance / Commercial Team

Needs visibility into revenue and freight-related order economics.

Key metrics:

- Revenue
- Freight Cost
- Freight Ratio
- Contribution Proxy
- Category-level performance

---

### Product / Category Manager

Needs to compare product categories and understand their commercial performance.

Key metrics:

- Category Revenue
- Average Product Price
- Freight Cost
- Freight Ratio
- Contribution Proxy

---

### Data / BI Analyst

Needs reliable and reproducible analytical outputs.

Key requirements:

- Data-quality validation
- SQL validation
- Consistent KPI definitions
- Reproducible ETL
- Python analytical outputs
- Power BI data model
- Dashboard calculation validation

---

## 4. Stakeholder Priority

| Stakeholder | Influence | Analytical Dependency | Priority |
|---|---|---|---|
| Business Manager | High | High | High |
| Operations Manager | High | High | High |
| Customer Experience Manager | Medium-High | High | High |
| CRM / Customer Analytics | Medium-High | High | High |
| Finance / Commercial | High | Medium-High | High |
| Product / Category Manager | Medium | Medium | Medium |
| Data / BI Analyst | High | High | High |

---

## 5. Stakeholder-to-Requirement Mapping

| Stakeholder | Related Requirements |
|---|---|
| Business Manager | BR-01, BR-12 |
| Operations Manager | BR-05, BR-06, BR-10 |
| Customer Experience Manager | BR-07, BR-10 |
| CRM / Customer Analytics | BR-02, BR-03, BR-04 |
| Finance / Commercial | BR-08 |
| Product / Category Manager | BR-09 |
| Data / BI Analyst | BR-11, BR-12 |

---

## 6. Communication and Reporting Needs

The analytical solution should present information at different levels:

### Executive Level

Focus on:

- KPI summary
- Business trends
- Major regional differences
- Areas requiring investigation

### Operational Level

Focus on:

- Fulfillment exceptions
- Delivery delays
- Regional performance
- Freight metrics

### Customer Analytics Level

Focus on:

- Customer segments
- Retention
- Churn risk
- Satisfaction

### Commercial Level

Focus on:

- Revenue
- Freight
- Product/category performance
- Contribution proxy

---

## 7. Stakeholder Success Criteria

The solution should enable stakeholders to:

- Access relevant KPIs.
- Filter and explore business performance.
- Identify areas requiring investigation.
- Compare regions and customer segments.
- Understand relationships between operational and customer metrics.
- Use analytical evidence to support business decisions.