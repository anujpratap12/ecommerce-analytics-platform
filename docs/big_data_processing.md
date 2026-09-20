# Big Data Processing with PySpark

## 1. Purpose

The project includes a PySpark-based Big Data processing extension to demonstrate distributed data processing concepts on the Olist Brazilian E-Commerce dataset.

The PySpark pipeline complements the primary Python, PostgreSQL, SQL, and Power BI analytics workflow by processing cleaned order and order-item datasets using Spark DataFrames.

---

## 2. Processing Architecture

```text
Cleaned Olist CSV Data
        |
        v
   PySpark SparkSession
        |
        v
   Spark DataFrames
        |
        v
Order + Order Item Join
        |
        v
Order-Level Aggregation
        |
        v
Customer-Level Aggregation
        |
        v
Spending Analysis
        |
        v
Customer Big Data Summary
        |
        v
CSV Analytical Report