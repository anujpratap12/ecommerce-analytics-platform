# GitHub Copilot Productivity Workflow

## 1. Purpose

GitHub Copilot was used as an AI-assisted development and code-review productivity tool during the PostgreSQL analytics work.

The workflow focused on improving data validation and query reliability without replacing human review or testing.

---

## 2. Development Task

The project required a repeatable validation process for the `analytics.order_analytics` table.

The validation requirements were:

- Detect duplicate `order_id` values
- Detect NULL `customer_state` values
- Detect NULL `order_total_value` values
- Detect negative `order_total_value` values

---

## 3. Copilot-Assisted Workflow

```text
Development Requirement
        |
        v
GitHub Copilot Analysis
        |
        v
Suggested Validation Approach
        |
        v
AI-Generated PostgreSQL SQL
        |
        v
Human Code Review
        |
        v
Refinement of Generated SQL
        |
        v
Implementation
        |
        v
PostgreSQL Execution
        |
        v
Validation Results