-- ============================================================
-- E-COMMERCE ANALYTICS PLATFORM
-- EXECUTIVE KPI ANALYSIS
-- ============================================================


-- ============================================================
-- 1. OVERALL BUSINESS KPIs
-- ============================================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    SUM(order_value) AS total_product_revenue,
    SUM(freight_cost) AS total_freight_cost,
    SUM(order_total_value) AS total_order_value,
    AVG(order_total_value) AS average_order_value,
    AVG(review_score) AS average_review_score,
    ROUND(
        AVG(is_late::numeric) * 100,
        2
    ) AS late_delivery_rate,
    ROUND(
        AVG(is_repeat_customer::numeric) * 100,
        2
    ) AS repeat_customer_rate
FROM analytics.order_analytics;


-- ============================================================
-- 2. MONTHLY BUSINESS PERFORMANCE
-- ============================================================

SELECT
    DATE_TRUNC(
        'month',
        order_purchase_timestamp
    )::date AS order_month,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(DISTINCT customer_unique_id)
        AS unique_customers,

    ROUND(
        SUM(order_value)::numeric,
        2
    ) AS product_revenue,

    ROUND(
        SUM(freight_cost)::numeric,
        2
    ) AS freight_cost,

    ROUND(
        SUM(order_total_value)::numeric,
        2
    ) AS total_order_value,

    ROUND(
        AVG(order_total_value)::numeric,
        2
    ) AS average_order_value

FROM analytics.order_analytics

GROUP BY 1

ORDER BY 1;


-- ============================================================
-- 3. MONTH-OVER-MONTH REVENUE GROWTH
-- ============================================================

WITH monthly_revenue AS (

    SELECT
        DATE_TRUNC(
            'month',
            order_purchase_timestamp
        )::date AS order_month,

        SUM(order_value) AS revenue

    FROM analytics.order_analytics

    GROUP BY 1
),

revenue_with_previous AS (

    SELECT
        order_month,
        revenue,

        LAG(revenue) OVER (
            ORDER BY order_month
        ) AS previous_month_revenue

    FROM monthly_revenue
)

SELECT
    order_month,

    ROUND(
        revenue::numeric,
        2
    ) AS revenue,

    ROUND(
        previous_month_revenue::numeric,
        2
    ) AS previous_month_revenue,

    ROUND(
        (
            (revenue - previous_month_revenue)
            / NULLIF(previous_month_revenue, 0)
        )::numeric * 100,
        2
    ) AS mom_growth_percentage

FROM revenue_with_previous

ORDER BY order_month;


-- ============================================================
-- 4. ORDER STATUS PERFORMANCE
-- ============================================================

SELECT
    order_status,

    COUNT(*) AS order_count,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_orders,

    ROUND(
        AVG(order_total_value)::numeric,
        2
    ) AS average_order_value

FROM analytics.order_analytics

GROUP BY order_status

ORDER BY order_count DESC;


-- ============================================================
-- 5. DELIVERY PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) FILTER (
        WHERE is_delivered = 1
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_late = 1
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE is_late = 0
        AND is_delivered = 1
    ) AS on_time_deliveries,

    ROUND(
        AVG(delivery_days)
        FILTER (
            WHERE is_delivered = 1
        )::numeric,
        2
    ) AS average_delivery_days,

    ROUND(
        AVG(delivery_delay_days)
        FILTER (
            WHERE is_delivered = 1
        )::numeric,
        2
    ) AS average_delivery_delay_days

FROM analytics.order_analytics;


-- ============================================================
-- 6. CUSTOMER RETENTION SNAPSHOT
-- ============================================================

SELECT
    COUNT(DISTINCT customer_unique_id)
        AS total_customers,

    COUNT(DISTINCT customer_unique_id)
        FILTER (
            WHERE is_repeat_customer = 1
        ) AS repeat_customers,

    ROUND(
        COUNT(DISTINCT customer_unique_id)
        FILTER (
            WHERE is_repeat_customer = 1
        ) * 100.0
        / COUNT(DISTINCT customer_unique_id),
        2
    ) AS repeat_customer_percentage

FROM analytics.order_analytics;


-- ============================================================
-- 7. CUSTOMER VALUE DISTRIBUTION
-- ============================================================

SELECT
    CASE
        WHEN monetary_value < 100
            THEN 'Low Value'

        WHEN monetary_value < 500
            THEN 'Medium Value'

        WHEN monetary_value < 1000
            THEN 'High Value'

        ELSE 'Very High Value'
    END AS customer_value_segment,

    COUNT(DISTINCT customer_unique_id)
        AS customer_count,

    ROUND(
        AVG(monetary_value)::numeric,
        2
    ) AS average_customer_value

FROM analytics.order_analytics

GROUP BY 1

ORDER BY
    average_customer_value;


-- ============================================================
-- 8. STATE-LEVEL PERFORMANCE
-- ============================================================

SELECT
    customer_state,

    COUNT(DISTINCT order_id)
        AS total_orders,

    COUNT(DISTINCT customer_unique_id)
        AS unique_customers,

    ROUND(
        SUM(order_value)::numeric,
        2
    ) AS product_revenue,

    ROUND(
        AVG(order_total_value)::numeric,
        2
    ) AS average_order_value,

    ROUND(
        AVG(is_late::numeric) * 100,
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS average_review_score

FROM analytics.order_analytics

GROUP BY customer_state

ORDER BY product_revenue DESC;


-- ============================================================
-- 9. TOP PRODUCT CATEGORIES
-- ============================================================

SELECT
    product_category_name_english
        AS product_category,

    COUNT(DISTINCT order_id)
        AS orders,

    COUNT(DISTINCT product_id)
        AS products_sold,

    ROUND(
        SUM(price)::numeric,
        2
    ) AS product_revenue,

    ROUND(
        SUM(freight_value)::numeric,
        2
    ) AS freight_cost

FROM analytics.order_item_analytics

GROUP BY product_category_name_english

ORDER BY product_revenue DESC

LIMIT 20;