# E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform

An end-to-end e-commerce analytics platform that transforms raw transactional data into business insights using Python, PostgreSQL, SQL, statistical analysis, customer analytics, machine learning, and Power BI.

The project analyzes approximately 100K e-commerce orders to understand customer retention, fulfillment performance, customer satisfaction, shipping-cost pressure, product performance, regional differences, and churn risk.

---

## 📌 Project Overview

E-commerce businesses generate large volumes of transactional, customer, product, payment, delivery, and review data. However, raw data alone does not provide clear answers to important business questions.

This project builds an end-to-end analytics platform to investigate:

- Why customers are not returning
- How delivery delays relate to customer satisfaction
- Which regions have higher fulfillment problems
- Where shipping costs create cost pressure
- Which product categories generate the most revenue
- Which customers show higher churn risk
- Which operational areas require further investigation

The project follows a complete workflow from raw data ingestion to data cleaning, ETL, database modeling, SQL analytics, statistical analysis, customer segmentation, churn-risk classification, Power BI visualization, and business recommendations.

---

# 🎯 Business Problem

The e-commerce business is experiencing challenges related to customer retention, fulfillment efficiency, customer satisfaction, and profitability pressure.

Potential contributing factors include:

- Late deliveries
- Longer delivery times
- High freight costs
- Poor customer satisfaction
- Low repeat-purchase behavior
- Uneven regional fulfillment performance
- Differences in product and category economics

The goal is to use data to identify these patterns and provide business-focused insights that can support operational and customer-retention decisions.

---

# 🎯 Business Objectives

The project focuses on five major analytical areas:

### 1. Customer Retention

- Analyze repeat purchasing behavior
- Understand customer purchase frequency
- Segment customers using RFM analysis
- Identify customers with higher churn risk

### 2. Fulfillment & Logistics

- Measure delivery performance
- Identify late-delivery patterns
- Analyze fulfillment risk
- Compare fulfillment performance across regions
- Understand freight-cost behavior

### 3. Customer Experience

- Analyze review scores
- Compare satisfaction between late and on-time deliveries
- Identify relationships between delivery performance and customer experience

### 4. Profitability & Cost Analysis

- Analyze order value and freight costs
- Measure freight burden using freight ratio
- Analyze contribution proxy
- Identify cost patterns across orders and categories

### 5. Product & Regional Performance

- Identify top-performing product categories
- Analyze product pricing
- Compare freight patterns
- Analyze regional performance differences

---

# 🏗️ End-to-End Architecture

```text
                    Olist E-Commerce Dataset
                              │
                              ▼
                       Raw CSV Data
                              │
                              ▼
                    Python Data Inspection
                              │
                              ▼
                 Data Cleaning & Validation
                              │
                              ▼
                     Feature Engineering
                              │
                              ▼
                        PostgreSQL
                 ┌────────────┼────────────┐
                 │            │            │
                Raw        Staging      Analytics
                 │            │            │
                 └────────────┼────────────┘
                              │
                              ▼
                       Advanced SQL
                          Analysis
                              │
                              ▼
                    Python EDA & Statistics
                              │
                              ▼
                 Customer & Churn Analytics
                              │
                              ▼
                     Power BI Data Model
                              │
                              ▼
                  Interactive Dashboards
                              │
                              ▼
                    Business Insights
                              │
                              ▼
                  Business Recommendations
```

---

# 📋 Business Analysis Layer

To complement the analytical workflow, the project includes a structured Business Analysis layer that translates the business problem into measurable analytical requirements and validates the resulting solution.

The documentation covers:

- **Business Requirements Document (BRD)** — business problem, objectives, stakeholders, KPIs, requirements, constraints, and success criteria.
- **Functional Requirements Document (FRD)** — functional/non-functional requirements, business rules, reporting requirements, and expected outputs.
- **Stakeholder Matrix** — stakeholder personas, information needs, KPIs, and dashboard mapping.
- **Process & Gap Analysis** — AS-IS process, identified business gaps, TO-BE analytical process, and gap-to-solution mapping.
- **User Stories & Acceptance Criteria** — business-user needs translated into testable requirements.
- **Data Dictionary & Data Mapping** — business meaning, source fields, KPI definitions, data lineage, and requirement-to-data mapping.
- **UAT Test Cases** — project-level acceptance scenarios for dashboards, KPIs, business rules, and analytical outputs.
- **Defect Log** — documented development/validation issues and their resolutions.
- **Change Request** — documented project-level requirement and analytical enhancements.
- **Requirements Traceability Matrix (RTM)** — links business requirements to functional requirements, user stories, analytical outputs, dashboards, and validation.

### Business-to-Analytics Traceability

**Business Problem → Requirements → User Stories → Data → Analytics → Dashboard → Validation → Business Insights**

> The BA artifacts represent project-defined stakeholder personas, requirements, and validation scenarios. They do not claim formal requirements gathering, stakeholder sign-off, or enterprise UAT experience.

---

# 🛠️ Technology Stack

### Programming & Data Analysis

- Python 3.14
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Statsmodels
- Scikit-learn

### Database & SQL

- PostgreSQL
- SQL
- SQLAlchemy
- psycopg2

### Business Intelligence

- Power BI Desktop
- Power Query
- DAX

### Supporting Tools

- Excel
- OpenPyXL
- Jupyter Notebook
- Git
- GitHub

### Business Analysis

- Business Requirements (BRD)
- Functional Requirements (FRD)
- Stakeholder Analysis
- User Stories
- Acceptance Criteria
- Process & Gap Analysis
- Data Mapping & Data Dictionary
- UAT
- Requirements Traceability
- Defect Tracking
- Change Management

---

# 📊 Dataset

## Olist Brazilian E-Commerce Public Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset containing approximately 100K orders from the Brazilian e-commerce marketplace.

The dataset contains information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translations

### Dataset Files

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

---

# 🔄 Data Engineering & ETL

The project implements a Python-based ETL pipeline that converts raw CSV data into analytics-ready datasets.

## ETL Workflow

```text
Extract
   ↓
Inspect
   ↓
Clean
   ↓
Validate
   ↓
Transform
   ↓
Feature Engineer
   ↓
Load into PostgreSQL
   ↓
Analyze
```

## Data Cleaning

The pipeline performs:

- Data inspection and profiling
- Missing-value analysis
- Duplicate detection
- Date parsing and standardization
- Text normalization
- Numerical validation
- Invalid-value detection
- Product category translation
- Review data preparation
- Order status analysis
- Delivery-date validation

## Data Quality Validation

The project validates:

- Duplicate records
- Missing values
- Invalid dates
- Negative prices
- Negative freight values
- Referential integrity
- Duplicate order IDs
- Duplicate customer IDs
- Product relationships
- Seller relationships
- Payment relationships
- Review relationships

Raw datasets are kept separate from processed datasets to preserve source-data integrity.

---

# 🗄️ PostgreSQL Data Architecture

PostgreSQL is used as the central analytical database.

## Database

```text
ecommerce_analytics
```

## Schemas

```text
raw
staging
analytics
```

## Staging Tables

```text
staging.customers
staging.orders
staging.order_items
staging.payments
staging.products
staging.reviews
staging.sellers
```

## Analytics Tables

```text
analytics.order_analytics
analytics.order_item_analytics
```

The staging layer stores cleaned source-level data, while the analytics layer contains business-ready features used for SQL analysis and Power BI reporting.

---

# 🧮 Feature Engineering

The project creates analytical features at order, customer, fulfillment, product, and geographic levels.

## Order-Level Features

- Order value
- Freight cost
- Total order value
- Freight ratio
- Delivery days
- Delivery delay days
- Late-delivery flag
- Delivered-order flag
- Fulfillment risk

## Customer-Level Features

- Customer lifetime orders
- Customer order number
- Recency
- Frequency
- Monetary value
- Average order value
- Repeat customer flag
- RFM segment
- Churn flag

## Product-Level Features

- Product category
- Product price
- Item total value
- Freight cost
- Freight ratio

## Geographic Features

- Seller state
- Customer state
- Seller-to-customer route

---

# 📈 SQL Analytics

PostgreSQL is used to perform analytical queries and generate business-level insights.

## Executive KPIs

- Total orders
- Total customers
- Product revenue
- Freight cost
- Total order value
- Average order value
- Average review score
- Delivered orders
- Late deliveries
- Late-delivery rate
- Repeat customers
- Repeat-customer rate

## Customer Retention Analysis

- One-time vs repeat customers
- Purchase frequency
- Customer lifetime value
- RFM segmentation
- Customer value segments
- Customer distribution by state

## Fulfillment & Logistics Analysis

- Average delivery duration
- Delivery delays
- Late-delivery rate
- Average freight cost
- Freight ratio
- Fulfillment-risk segmentation
- State-level fulfillment performance

## Customer Experience Analysis

- Review score distribution
- Low-satisfaction orders
- Late vs on-time satisfaction
- Delivery performance vs review scores

## Product Analysis

- Revenue by product category
- Product pricing
- Freight cost by category
- Freight ratio
- Category-level performance

---

# 🐍 Python Exploratory Data Analysis

Python is used for deeper exploratory analysis and statistical validation.

## EDA Areas

- Order distribution
- Customer purchasing behavior
- Delivery performance
- Freight-cost distribution
- Product category performance
- Regional performance
- Customer value segmentation
- Correlation analysis
- Outlier detection

## Outlier Detection

IQR-based analysis is used to identify potential outliers in:

- Order value
- Freight cost
- Delivery duration
- Delivery delay

Outliers are analyzed as potential business signals rather than automatically treated as data errors.

---

# 📐 Statistical Analysis

Statistical methods are used to validate relationships observed during exploratory analysis.

## Methods Used

- Pearson correlation
- Spearman correlation
- Welch's t-test
- Mann-Whitney U test
- Chi-square test
- Confidence intervals

## Key Statistical Findings

- Delivery duration is negatively associated with customer review scores.
- Delivery delay is negatively associated with customer review scores.
- Late-delivery orders have substantially lower average review scores than on-time or early orders.
- Low satisfaction is considerably more common among late-delivery orders.
- Freight cost has a positive relationship with order value.
- Freight ratio tends to decrease as order value increases.

These findings represent statistical associations and should not be interpreted as proof of causation.

---

# 👥 Customer Retention & RFM Analysis

Customer purchasing behavior is analyzed using:

- Recency
- Frequency
- Monetary value

Customers are segmented using RFM-based business rules.

## RFM Segments

```text
High Value Active
Loyal
Active
At Risk - High Value
At Risk
Inactive
```

RFM segmentation helps identify customers with different engagement and value profiles and provides a foundation for targeted retention analysis.

---

# 🤖 Churn-Risk Classification

The project includes a customer-level churn-risk classification model using Logistic Regression.

The original Olist dataset does not contain an explicit churn label, so churn is analytically defined using customer recency.

## Churn Definition

```text
Churn = Recency > 180 days
```

## Model Features

- Average delivery days
- Late-delivery rate
- Total freight
- Total order value
- Average order value
- Average freight ratio
- Average review score
- Low-satisfaction rate
- Total orders

## Model Performance

```text
Accuracy  : 60.30%
Precision : 82.62%
Recall    : 55.58%
F1 Score  : 66.45%
ROC-AUC   : 68.26%
```

## Feature Importance

Permutation importance indicated that average delivery days was the strongest predictive feature among the modeled variables.

## Churn Risk Segments

```text
Low Risk
Medium Risk
High Risk
```

---

# ⚠️ Churn Model Limitation

The current churn classification is intended as an analytical portfolio exercise and should be interpreted as a risk-classification analysis rather than a production decisioning system.

The churn label is based on customer recency, while the model uses customer-level historical features. Because the current implementation uses full-history customer information, it should not be treated as a production-ready forward-looking churn model.

A production implementation would require a temporal snapshot approach, where customer features are calculated using data available before the prediction period and churn is measured in a subsequent observation window.

---

# 📊 Power BI Dashboard

The Power BI dashboard contains six analytical pages designed around business questions.

The repository includes screenshots of all six dashboard pages under `docs/screenshots/`. The editable `.pbix` file is retained locally rather than committed to the public repository.

## 1️⃣ Executive Overview

### KPIs

- Total Orders
- Total Revenue
- Total Freight Cost
- Total Customers
- Average Review Score
- Late Delivery Rate
- Average Order Value

### Visualizations

- Monthly order trends
- Revenue by customer state
- Executive KPI cards

## 2️⃣ Customer Retention

### KPIs

- Repeat Customers
- Repeat Customer Rate

### Visualizations

- Purchase frequency
- RFM segments
- Customer distribution by state
- Churn by RFM segment

## 3️⃣ Fulfillment & Logistics

### KPIs

- Late Delivery Rate
- Average Delivery Days
- Average Freight Cost

### Visualizations

- Orders by fulfillment risk
- Late vs on-time orders
- Late delivery rate by state
- Customer satisfaction: late vs on-time delivery
- Average delivery days by month

## 4️⃣ Customer Experience

### KPI

- Average Review Score

### Visualizations

- Review score distribution
- Low satisfaction: late vs on-time
- Average review score trend

## 5️⃣ Profitability & Product Performance

### KPIs

- Contribution Proxy
- Average Freight Ratio

### Visualizations

- Product/category revenue analysis
- Average product price by category
- Product price vs freight cost
- Top product categories by revenue

## 6️⃣ Root Cause Analysis

### Visualizations

- States with highest late-delivery rates
- Low satisfaction across fulfillment-risk segments
- Review score: late vs on-time delivery

---

# 📌 Key Business Findings

### 1. Delivery Performance & Customer Satisfaction

Late deliveries are associated with substantially lower customer review scores, making fulfillment performance an important customer-experience signal.

### 2. Delivery Duration

Longer delivery durations show a negative relationship with review scores.

### 3. Late Deliveries & Low Satisfaction

Low-satisfaction orders occur much more frequently among late deliveries than among on-time or early deliveries.

### 4. Regional Fulfillment Differences

Late-delivery rates vary considerably across Brazilian states, indicating that fulfillment performance should be analyzed geographically.

### 5. Freight Cost Pressure

Lower-value orders generally have a higher freight-cost burden relative to order value. Freight ratio is therefore a useful metric for monitoring shipping-cost pressure.

### 6. Customer Retention

The majority of customers made only one purchase in the available dataset, highlighting the importance of understanding repeat-purchase behavior.

### 7. Product Category Performance

Product categories contribute differently to overall revenue and order economics, making category-level analysis useful for product and pricing decisions.

---

# 💡 Business Recommendations

## Fulfillment

- Investigate states with consistently high late-delivery rates.
- Monitor delivery duration by geography.
- Prioritize high-risk fulfillment areas for operational investigation.
- Track late-delivery rate as a core operational KPI.

## Customer Experience

- Monitor customer satisfaction alongside delivery performance.
- Identify severely delayed orders for potential service recovery.
- Use review-score trends to detect changes in customer experience.

## Customer Retention

- Identify high-value customers showing signs of disengagement.
- Use RFM segmentation for targeted retention analysis.
- Analyze fulfillment experience as a potential retention signal.

## Cost Management

- Monitor freight ratio for lower-value orders.
- Compare freight costs across states and product categories.
- Investigate categories with unusually high shipping-cost burden.

## Product Strategy

- Monitor high-performing product categories.
- Compare product prices with associated freight costs.
- Use category-level analytics to support pricing and product decisions.

---

# 💰 Contribution Proxy

The Olist dataset does not contain product acquisition costs, operating expenses, taxes, marketing costs, or other financial components required to calculate true accounting profit.

Therefore, the project uses an analytical contribution proxy:

```text
Contribution Proxy = Order Value - Freight Cost
```

This metric represents order value after freight cost only.

It should not be interpreted as net profit or true accounting contribution margin.

---

# ⚠️ Dataset Limitations

The original dataset does not provide:

- Actual carrier names
- Warehouse identifiers
- Marketing campaign data
- Customer acquisition cost
- Product acquisition cost
- Operating expenses
- Taxes
- Explicit churn labels
- True accounting profit

Therefore, metrics such as churn and contribution proxy are analytical constructs derived from the available data.

---

# 📊 Project Metrics

Based on the current analytical dataset:

```text
Total Orders            : 99,441
Total Customers         : 96,096
Product Revenue         : 13,591,643.70
Freight Cost            : 2,251,909.54
Total Order Value       : 15,843,553.24
Average Product Revenue per Order : 136.68
Average Total Order Value (incl. freight) : 159.33
Average Review Score    : 4.09
Delivered Orders        : 96,476
Late Deliveries         : 7,827
Late Delivery Rate      : 8.11%
Repeat Customers        : 2,997
Repeat Customer Rate    : 3.12%
```

---

# 📋 Data Quality Validation Results

The project validates:

```text
✓ Duplicate records
✓ Missing values
✓ Invalid dates
✓ Negative prices
✓ Negative freight values
✓ Referential integrity
✓ Duplicate order IDs
✓ Duplicate customer IDs
✓ Product relationships
✓ Seller relationships
✓ Payment relationships
✓ Review relationships
```

Validated analytical data includes:

```text
99,441 orders
96,096 customers
112,650 order items
32,951 products
3,095 sellers
103,886 payment records
99,224 review records
```

---

# 📁 Project Structure

```text
ecommerce-analytics-platform/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── etl/
│   ├── __init__.py
│   ├── data_quality.py
│   ├── clean_data.py
│   ├── build_features.py
│   └── load_postgres.py
│
├── python/
│   ├── db_connection.py
│   ├── eda_analysis.py
│   └── churn_model.py
│
├── sql/
│   └── ...
│
├── powerbi/
│   └── ECommerce_Analytics_Platform.pbix
│
├── excel/
│   └── ...
│
├── reports/
│   ├── eda/
│   └── figures/
│
├── docs/
│   └── ...
│
├── README.md
├── requirements.txt
├── .gitignore
└── .venv/
```

---

# 🚀 How to Run the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd ecommerce-analytics-platform
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure PostgreSQL

Create a PostgreSQL database:

```text
ecommerce_analytics
```

Create the required schemas:

```sql
CREATE SCHEMA raw;
CREATE SCHEMA staging;
CREATE SCHEMA analytics;
```

Configure the database connection using environment variables:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_analytics
DB_USER=postgres
DB_PASSWORD=your_password
```

## 5. Run Data Quality Validation

```bash
python etl/data_quality.py
```

## 6. Run Data Cleaning

```bash
python etl/clean_data.py
```

## 7. Run Feature Engineering

```bash
python etl/build_features.py
```

## 8. Load Data into PostgreSQL

```bash
python etl/load_postgres.py
```

## 9. Run Exploratory Data Analysis

```bash
python python/eda_analysis.py
```

## 10. Run Churn-Risk Classification

```bash
python python/churn_model.py
```

## 11. Open Power BI

The editable Power BI `.pbix` file is maintained locally.

```text
powerbi/ECommerce_Analytics_Platform.pbix
```

Refresh the PostgreSQL data connection if required.

Dashboard screenshots are available in:

```text
docs/screenshots/
```

---

# 🔐 Data & Repository Practices

The repository keeps raw and processed datasets outside version control where appropriate.

Sensitive configuration files such as environment variables are excluded from Git.

The `.gitignore` file prevents accidental commits of:

- Virtual environments
- Environment files
- Raw datasets
- Processed datasets
- IDE files
- Temporary files
- Notebook checkpoints
- Power BI template files

Business Analysis documentation is version-controlled under:

```text
docs/business_analysis/
```

---

# ❓ Business Questions Answered

## Customer Analytics

- How many customers return?
- What does customer purchase frequency look like?
- Which customer segments have higher value?
- Which customers show higher churn risk?

## Fulfillment

- What percentage of orders are delivered late?
- Which states have higher late-delivery rates?
- How long does delivery typically take?
- Which orders fall into higher fulfillment-risk segments?

## Customer Experience

- How does delivery performance relate to review scores?
- Are late deliveries associated with lower satisfaction?
- Which fulfillment segments show higher low-satisfaction rates?

## Cost

- How much freight cost is generated?
- How does freight relate to order value?
- Which orders have a high freight burden?

## Product

- Which categories generate the most revenue?
- How do product prices vary by category?
- How does product price relate to freight cost?

---

# 💼 Business & Analytical Outcomes

The platform supports business users in:

- Monitoring executive KPIs and business trends.
- Identifying regions with higher fulfillment issues.
- Understanding the relationship between delivery performance and customer satisfaction.
- Segmenting customers using RFM analysis.
- Identifying analytical churn-risk segments.
- Evaluating product/category revenue performance.
- Monitoring freight cost and order economics.
- Investigating operational root causes.
- Translating business objectives into measurable requirements and KPIs.
- Validating analytical outputs through documented testing and project-level UAT scenarios.

The solution is designed as a decision-support platform: analytical findings highlight patterns and areas for investigation rather than claiming causal explanations or guaranteed business outcomes.

---

# 🚀 Project Outcome

This project demonstrates a complete end-to-end analytics workflow:

**Data Collection → Data Cleaning → Data Quality → ETL → PostgreSQL → SQL Analytics → Python EDA → Statistical Analysis → Customer Segmentation → Churn-Risk Classification → Power BI → Business Insights → Recommendations**

The project demonstrates how raw transactional data can be transformed into a structured analytics solution that supports business decision-making.

---

# ⭐ Project Highlights

- End-to-end analytics workflow
- Approximately 100K e-commerce orders
- Python-based ETL pipeline
- PostgreSQL analytical database
- Advanced SQL analysis
- Data quality validation
- Feature engineering
- Exploratory data analysis
- Statistical hypothesis testing
- RFM customer segmentation
- Churn-risk classification
- Power BI dashboard with six analytical pages
- Fulfillment and logistics analysis
- Customer experience analysis
- Product and regional performance analysis
- Business-focused root-cause analysis
- Action-oriented business recommendations
- Reproducible project structure
- Business requirements and functional requirements documentation
- Stakeholder analysis and process/gap analysis
- User stories and acceptance criteria
- UAT, defect and change documentation
- End-to-end requirements traceability

---

# 🎓 Skills Demonstrated

```text
Python
Pandas
NumPy
SQL
PostgreSQL
ETL
Data Cleaning
Data Quality
Feature Engineering
Exploratory Data Analysis
Statistical Analysis
Scikit-learn
Logistic Regression
Customer Analytics
RFM Analysis
Churn Analysis
Power BI
Power Query
DAX
Excel
Data Visualization
Business Intelligence
Data Modeling
Business Requirements
Functional Requirements
Stakeholder Analysis
User Stories
Acceptance Criteria
Process & Gap Analysis
UAT
Requirements Traceability
Defect Tracking
Change Management
Git
GitHub
```

---

# 👨‍💻 Author

**Anuj Pratap Singh**

B.Tech Computer Science & Engineering  
Artificial Intelligence & Machine Learning

GitHub: https://github.com/anujpratap12

---

# 📌 Final Summary

This project brings together data engineering, analytics, statistics, machine learning, and business intelligence into one end-to-end e-commerce analytics solution.

The platform provides a complete path from:

**Raw Data → Clean Data → Database → SQL → Python Analysis → Customer Analytics → Churn Risk → Power BI → Business Insights**

The primary focus is on understanding the relationship between **fulfillment performance, customer satisfaction, retention, shipping costs, and business value** using a reproducible and business-oriented analytical workflow.
