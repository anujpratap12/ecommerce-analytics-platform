# Defect Log

## 1. Purpose

This document records issues identified during development, validation, and dashboard implementation of the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform.

The purpose is to demonstrate a structured approach to identifying, documenting, resolving, and validating analytical/reporting issues.

> Note: This is a project-level defect log and does not represent defects raised in a production enterprise environment.

---

## 2. Defect Register

| Defect ID | Area | Issue | Severity | Resolution | Status |
|---|---|---|---|---|---|
| DEF-001 | Power BI | Date-based visual did not display correctly because order timestamps included time components | Medium | Created a date-only field and established the appropriate DateTable relationship | Resolved |
| DEF-002 | Power BI | Monthly reporting required chronological sorting | Low | Created Year Month Sort and configured Year Month sorting | Resolved |
| DEF-003 | Data Validation | Source datasets contained missing values in selected fields | Medium | Missing-value patterns were assessed and documented during data-quality processing | Resolved |
| DEF-004 | Data Quality | Geolocation dataset contained duplicate records | Low | Duplicate records were identified during data-quality assessment | Resolved |
| DEF-005 | Analytical Modeling | Churn model required a clearly documented interpretation because churn was analytically derived | Medium | Churn definition and model limitation were documented | Resolved |
| DEF-006 | Business Metrics | Profitability could not be calculated as accounting profit from the available dataset | Medium | Contribution Proxy was introduced and explicitly documented as a profitability-related proxy | Resolved |

---

# 3. Defect Severity

| Severity | Definition |
|---|---|
| High | Issue prevents a major business function or produces materially incorrect results |
| Medium | Issue affects an analytical/reporting function but does not prevent overall project operation |
| Low | Minor usability, formatting, or documentation issue |

---

# 4. Defect Lifecycle

The project follows the following defect-management process:

Issue Identified
↓
Issue Documented
↓
Severity Assessed
↓
Root Cause Investigated
↓
Resolution Implemented
↓
Output Validated
↓
Defect Closed

---

# 5. Validation After Resolution

Resolved issues were rechecked through appropriate validation activities including:

- Power BI visual verification.
- Relationship validation.
- SQL validation.
- Python data-quality checks.
- Automated Python tests.
- Dashboard output review.

---

# 6. Defect Management Principles

Defects should be:

- Clearly documented.
- Assigned an appropriate severity.
- Investigated before resolution.
- Resolved using reproducible changes.
- Revalidated after resolution.
- Closed only after expected behavior is confirmed.