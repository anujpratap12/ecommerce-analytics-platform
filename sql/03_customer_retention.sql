-- ============================================================
-- 03 CUSTOMER RETENTION & RFM ANALYSIS
-- ============================================================


-- ============================================================
-- 1. ONE-TIME VS REPEAT CUSTOMERS
-- ============================================================

WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM analytics.order_analytics
    GROUP BY customer_unique_id
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS customers,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM customer_orders

GROUP BY 1

ORDER BY customers DESC;


-- ============================================================
-- 2. PURCHASE FREQUENCY SUMMARY
-- ============================================================

WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM analytics.order_analytics
    GROUP BY customer_unique_id
)

SELECT
    CASE
        WHEN order_count = 1 THEN '1 Order'
        WHEN order_count = 2 THEN '2 Orders'
        WHEN order_count BETWEEN 3 AND 5 THEN '3-5 Orders'
        ELSE '6+ Orders'
    END AS purchase_frequency_group,

    COUNT(*) AS customers,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM customer_orders

GROUP BY 1

ORDER BY MIN(order_count);


-- ============================================================
-- 3. COHORT RETENTION SUMMARY
-- Only key retention milestones are displayed
-- ============================================================

WITH customer_activity AS (

    SELECT DISTINCT
        customer_unique_id,

        DATE_TRUNC(
            'month',
            order_purchase_timestamp
        )::date AS activity_month

    FROM analytics.order_analytics
),

customer_cohort AS (

    SELECT
        customer_unique_id,

        MIN(activity_month) AS cohort_month

    FROM customer_activity

    GROUP BY customer_unique_id
),

cohort_activity AS (

    SELECT
        cc.cohort_month,

        (
            EXTRACT(YEAR FROM ca.activity_month)
            - EXTRACT(YEAR FROM cc.cohort_month)
        ) * 12
        +
        (
            EXTRACT(MONTH FROM ca.activity_month)
            - EXTRACT(MONTH FROM cc.cohort_month)
        ) AS months_since_first_purchase,

        COUNT(DISTINCT ca.customer_unique_id)
            AS active_customers

    FROM customer_activity ca

    JOIN customer_cohort cc
        ON ca.customer_unique_id =
           cc.customer_unique_id

    GROUP BY
        cc.cohort_month,
        ca.activity_month
),

cohort_size AS (

    SELECT
        cohort_month,

        COUNT(*) AS cohort_customers

    FROM customer_cohort

    GROUP BY cohort_month
)

SELECT
    ca.cohort_month,

    ca.months_since_first_purchase::integer
        AS month_number,

    ca.active_customers,

    cs.cohort_customers,

    ROUND(
        ca.active_customers * 100.0
        / cs.cohort_customers,
        2
    ) AS retention_percentage

FROM cohort_activity ca

JOIN cohort_size cs
    ON ca.cohort_month =
       cs.cohort_month

WHERE ca.months_since_first_purchase IN (0, 1, 3, 6, 12)

ORDER BY
    ca.cohort_month,
    ca.months_since_first_purchase;


-- ============================================================
-- 4. RFM CUSTOMER SEGMENT SUMMARY
-- ============================================================

WITH customer_rfm AS (

    SELECT
        customer_unique_id,

        MAX(order_purchase_timestamp)
            AS last_purchase,

        COUNT(DISTINCT order_id)
            AS frequency,

        SUM(order_total_value)
            AS monetary_value

    FROM analytics.order_analytics

    GROUP BY customer_unique_id
),

reference_date AS (

    SELECT
        MAX(order_purchase_timestamp)
        + INTERVAL '1 day'
            AS analysis_date

    FROM analytics.order_analytics
),

rfm AS (

    SELECT
        c.customer_unique_id,

        (
            r.analysis_date
            - c.last_purchase
        )::integer AS recency,

        c.frequency,

        c.monetary_value,

        NTILE(5) OVER (
            ORDER BY
                r.analysis_date
                - c.last_purchase
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY c.frequency
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY c.monetary_value
        ) AS m_score

    FROM customer_rfm c

    CROSS JOIN reference_date r
),

segmented AS (

    SELECT
        *,

        CASE

            WHEN r_score >= 4
             AND f_score >= 4
             AND m_score >= 4
                THEN 'High Value Active'

            WHEN r_score >= 4
             AND f_score >= 3
                THEN 'Loyal Customers'

            WHEN r_score <= 2
             AND f_score >= 3
                THEN 'At Risk'

            WHEN r_score <= 2
             AND m_score >= 4
                THEN 'High Value At Risk'

            WHEN r_score >= 4
             AND f_score <= 2
                THEN 'New / Potential'

            ELSE 'Regular Customers'

        END AS customer_segment

    FROM rfm
)

SELECT
    customer_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(recency)::numeric,
        1
    ) AS avg_recency_days,

    ROUND(
        AVG(frequency)::numeric,
        2
    ) AS avg_frequency,

    ROUND(
        AVG(monetary_value)::numeric,
        2
    ) AS avg_customer_value,

    ROUND(
        SUM(monetary_value)::numeric,
        2
    ) AS total_customer_value

FROM segmented

GROUP BY customer_segment

ORDER BY total_customer_value DESC;