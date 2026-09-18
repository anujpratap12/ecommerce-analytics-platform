# Data Dictionary & Data Mapping

## 1. Purpose

This document defines the key analytical fields used by the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform and maps them to their business meaning, source data, and analytical usage.

The data dictionary supports consistent KPI definitions, analytical transparency, and traceability between business requirements and the underlying data.

---

# 2. Core Data Entities

The project uses the following primary entities:

| Entity | Description |
|---|---|
| Customer | Customer identity and geographic information |
| Order | Order lifecycle and delivery information |
| Order Item | Products purchased within an order |
| Payment | Payment method and transaction information |
| Review | Customer satisfaction and review information |
| Product | Product attributes and category information |
| Seller | Seller identity and geographic information |
| Geolocation | Geographic information associated with postal codes |

---

# 3. Customer Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| customer_id | Unique customer record associated with an order | Customer/order relationship |
| customer_unique_id | Unique customer identifier across orders | Customer-level analysis |
| customer_zip_code_prefix | Customer postal code prefix | Geographic analysis |
| customer_city | Customer city | Geographic analysis |
| customer_state | Customer state | Regional analysis |

---

# 4. Order Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| order_id | Unique order identifier | Order counting |
| customer_unique_id | Customer associated with order | Customer analysis |
| order_status | Current/historical order status | Order lifecycle analysis |
| order_purchase_timestamp | Order purchase date/time | Time-series analysis |
| order_approved_at | Payment/order approval timestamp | Order lifecycle analysis |
| order_delivered_carrier_date | Date handed to carrier | Fulfillment analysis |
| order_delivered_customer_date | Customer delivery date | Delivery analysis |
| order_estimated_delivery_date | Estimated delivery date | Delivery performance |
| is_delivered | Delivery status indicator | Delivered-order analysis |
| delivery_days | Time taken to deliver order | Fulfillment KPI |
| delivery_delay_days | Difference between actual and estimated delivery | Delay analysis |
| is_late | Indicates whether delivery occurred after estimate | Late delivery KPI |
| order_value | Product/order item revenue associated with the order | Revenue analysis |
| freight_cost | Freight/shipping cost | Cost analysis |
| order_total_value | Order value including freight | Order economics |
| contribution_proxy | Order value less freight cost | Profitability-related proxy |

---

# 5. Customer Behavioral Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| customer_order_number | Sequential order number for a customer | Purchase behavior |
| customer_lifetime_orders | Total observed orders for customer | Frequency analysis |
| customer_recency_days | Days since customer's latest observed purchase | Retention/churn analysis |
| customer_frequency | Customer purchase frequency | RFM analysis |
| customer_monetary_value | Customer observed monetary value | RFM analysis |
| is_repeat_customer | Indicates customer has more than one observed order | Retention analysis |
| is_churned | Analytical churn indicator based on recency threshold | Churn-risk analysis |
| RFM Segment | Customer segment based on recency, frequency and monetary value | Customer segmentation |

---

# 6. Review Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| review_id | Unique review identifier | Review analysis |
| order_id | Order associated with review | Order/review relationship |
| review_score | Customer review score | Satisfaction KPI |
| review_comment_title | Customer review title | Qualitative review context |
| review_comment_message | Customer review message | Qualitative review context |
| is_low_satisfaction | Indicates review score of 1 or 2 | Low-satisfaction analysis |

---

# 7. Product Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| product_id | Unique product identifier | Product analysis |
| product_category_name | Product category | Category analysis |
| product_category_name_english | Translated product category | Business reporting |
| product_weight_g | Product weight | Product analysis |
| product_length_cm | Product length | Product analysis |
| product_height_cm | Product height | Product analysis |
| product_width_cm | Product width | Product analysis |

---

# 8. Order Item Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| order_id | Order containing the item | Order analysis |
| order_item_id | Item sequence within order | Item-level analysis |
| product_id | Product purchased | Product analysis |
| seller_id | Seller fulfilling item | Seller analysis |
| shipping_limit_date | Seller shipping deadline | Fulfillment analysis |
| price | Product/item price | Revenue and product analysis |
| freight_value | Freight associated with item | Shipping cost analysis |
| item_total_value | Item price plus freight | Order economics |

---

# 9. Seller Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| seller_id | Unique seller identifier | Seller analysis |
| seller_zip_code_prefix | Seller postal code prefix | Geographic analysis |
| seller_city | Seller city | Geographic analysis |
| seller_state | Seller state | Regional analysis |

---

# 10. Payment Fields

| Field | Business Meaning | Analytical Usage |
|---|---|---|
| order_id | Order associated with payment | Order/payment relationship |
| payment_sequential | Payment sequence | Payment analysis |
| payment_type | Payment method | Payment analysis |
| payment_installments | Number of installments | Payment behavior |
| payment_value | Payment value | Payment analysis |

---

# 11. Key KPI Definitions

| KPI | Definition | Primary Data |
|---|---|---|
| Total Orders | Distinct count of orders | Order |
| Total Customers | Distinct count of customer_unique_id | Customer/Order |
| Total Revenue | Sum of order value | Order |
| Total Freight Cost | Sum of freight cost | Order |
| Average Order Value | Revenue divided by total orders | Order |
| Average Review Score | Average review score | Review/Order |
| Late Delivery Rate | Late delivered orders divided by delivered orders | Order |
| Average Delivery Days | Average delivery duration for delivered orders | Order |
| Repeat Customer Rate | Repeat customers divided by observed customers | Customer |
| Contribution Proxy | Revenue/order value less freight cost | Order/Order Item |
| Low Satisfaction Rate | Low-satisfaction observations divided by applicable reviews | Review |

---

# 12. Business Rule Mapping

| Business Rule | Data Fields |
|---|---|
| Late Delivery | order_delivered_customer_date, order_estimated_delivery_date, is_late |
| Low Satisfaction | review_score, is_low_satisfaction |
| Repeat Customer | customer_unique_id, customer_lifetime_orders, is_repeat_customer |
| Analytical Churn | customer_recency_days, is_churned |
| RFM Segmentation | customer_recency_days, customer_frequency, customer_monetary_value |
| Contribution Proxy | order_value, freight_cost, contribution_proxy |

---

# 13. Requirement-to-Data Mapping

| Requirement | Required Data | Analytical Output |
|---|---|---|
| BR-01 Executive KPIs | Orders, customers, revenue, freight, reviews | Executive Overview |
| BR-02 Retention | Customer and order history | Retention analysis |
| BR-03 RFM Segmentation | Recency, frequency, monetary value | RFM segments |
| BR-04 Churn Risk | Customer behavior and recency | Churn-risk classification |
| BR-05 Fulfillment | Delivery and freight fields | Fulfillment dashboard |
| BR-06 Regional Performance | Customer state, delivery fields | State-level analysis |
| BR-07 Customer Satisfaction | Review score, delivery status | Customer Experience dashboard |
| BR-08 Revenue/Freight | Order value, freight cost | Order economics |
| BR-09 Product Performance | Product/category, price, freight | Product analysis |
| BR-10 Root Cause Analysis | Delivery, satisfaction, regional metrics | Root Cause Analysis |

---

# 14. Data Lineage

The primary analytical lineage is:

Olist CSV Dataset
↓
Python Data Cleaning
↓
Processed Analytical Data
↓
PostgreSQL Staging Tables
↓
PostgreSQL Analytical Tables
↓
SQL Analysis
↓
Python Analysis
↓
Power BI Data Model
↓
Dashboard KPIs and Visualizations

---

# 15. Data Quality Considerations

The project validates:

- Missing values.
- Duplicate records.
- Invalid numeric values.
- Invalid dates.
- Referential integrity.
- Duplicate business keys.
- Unexpected categorical values.

Known source-data limitations are documented separately in the project README and analytical documentation.

---

# 16. Data Availability Limitations

The dataset does not contain:

- Explicit carrier names.
- Warehouse identifiers.
- Marketing campaign information.
- Customer acquisition cost.
- Complete product acquisition cost.
- Complete operating expenses.
- Accounting profit.

Therefore:

- Carrier-level performance cannot be directly analyzed.
- Warehouse-level performance cannot be directly analyzed.
- Marketing attribution cannot be directly analyzed.
- True accounting profit cannot be calculated.
- Contribution Proxy is used only as a profitability-related analytical metric.

---

# 17. Documentation Principle

Business metrics should be calculated from documented fields and definitions so that the same business concept can be consistently interpreted across Python, SQL, and Power BI.