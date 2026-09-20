# AI-Assisted SQL Generation and Validation

## 1. Purpose

This project demonstrates an AI-assisted SQL workflow for translating business questions into PostgreSQL queries.

The generated SQL was reviewed manually and executed against the project's `analytics.order_analytics` table to validate the query logic and results.

---

## 2. Business Question

The business question used for the demonstration was:

> Compare customer states by order volume and average order value. Return the number of distinct orders and average order value for each customer state. Include only states with at least 100 orders, sort by order volume descending, and return the top 10 states.

---

## 3. AI-Assisted Workflow

The workflow followed these steps:

```text
Business Question
        |
        v
Natural-Language Prompt
        |
        v
AI-Assisted SQL Generation
        |
        v
Manual SQL Review
        |
        v
PostgreSQL Execution
        |
        v
Result Validation