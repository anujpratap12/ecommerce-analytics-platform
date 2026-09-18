# Change Request

## 1. Purpose

This document demonstrates the change-management approach used for enhancements and requirement refinements during development of the E-Commerce Fulfillment, Customer Retention & Profitability Analytics Platform.

> Note: These are project-level change requests and do not represent formal requests from external organizational stakeholders.

---

# 2. Change Request Register

| Change ID | Change Description | Reason | Impact | Status |
|---|---|---|---|---|
| CR-001 | Add date-only field for order reporting | Improve compatibility between order timestamps and DateTable | Power BI time-series reporting | Implemented |
| CR-002 | Add Year Month Sort field | Ensure monthly visuals display chronologically | Reporting usability | Implemented |
| CR-003 | Add RFM segmentation | Improve customer retention analysis | Customer Retention dashboard | Implemented |
| CR-004 | Add churn-risk classification | Provide analytical customer risk segmentation | Customer Retention analysis | Implemented |
| CR-005 | Add fulfillment-risk analysis | Support operational investigation | Fulfillment & Root Cause dashboards | Implemented |
| CR-006 | Add contribution proxy | Provide profitability-related order economics despite unavailable complete cost data | Profitability dashboard | Implemented |
| CR-007 | Add Root Cause Analysis dashboard | Connect operational performance with customer satisfaction | Business decision support | Implemented |

---

# 3. Change Evaluation Process

Each proposed change is evaluated using:

1. Business value.
2. Analytical relevance.
3. Data availability.
4. Implementation effort.
5. Impact on existing dashboards.
6. Data consistency.
7. Testing requirements.

---

# 4. Change Lifecycle

Change Identified
↓
Business Need Evaluated
↓
Impact Assessed
↓
Change Implemented
↓
Testing Performed
↓
Documentation Updated
↓
Change Closed

---

# 5. Change Impact Assessment

Changes are reviewed for their potential impact on:

### Data

Whether new fields or transformations are required.

### Analytics

Whether existing calculations or analytical outputs are affected.

### Reporting

Whether dashboard visuals or KPIs need modification.

### Requirements

Whether BRD, FRD, user stories, or acceptance criteria need updates.

### Testing

Whether additional validation or UAT scenarios are required.

---

# 6. Change Control Principle

Changes should improve the ability of the platform to answer defined business questions without introducing unsupported assumptions or inconsistent metrics.

All analytical limitations should remain documented when the available source data does not support a requested business metric.