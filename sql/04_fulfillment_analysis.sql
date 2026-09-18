-- ============================================================
-- 04_FULFILLMENT_ANALYSIS.SQL
-- E-Commerce Fulfillment, Customer Retention & Profitability
-- ============================================================

-- ============================================================
-- 1. OVERALL FULFILLMENT PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_late = 1
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE is_late = 0
    ) AS on_time_orders,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(delivery_delay_days)::numeric,
        2
    ) AS avg_delivery_delay_days,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(freight_ratio)::numeric,
        4
    ) AS avg_freight_ratio

FROM analytics.order_analytics

WHERE is_delivered = 1;


-- ============================================================
-- 2. DELIVERY DELAY SEVERITY
-- ============================================================

WITH delay_categories AS (
    SELECT
        order_id,
        delivery_delay_days,

        CASE
            WHEN delivery_delay_days <= 0
                THEN 'On Time / Early'

            WHEN delivery_delay_days BETWEEN 1 AND 3
                THEN '1-3 Days Late'

            WHEN delivery_delay_days BETWEEN 4 AND 7
                THEN '4-7 Days Late'

            WHEN delivery_delay_days BETWEEN 8 AND 14
                THEN '8-14 Days Late'

            ELSE '15+ Days Late'
        END AS delay_category

    FROM analytics.order_analytics

    WHERE is_delivered = 1
)

SELECT
    delay_category,

    COUNT(*) AS orders,

    ROUND(
        100.0 * COUNT(*)
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_orders,

    ROUND(
        AVG(delivery_delay_days)::numeric,
        2
    ) AS avg_delay_days

FROM delay_categories

GROUP BY delay_category

ORDER BY
    CASE delay_category
        WHEN 'On Time / Early' THEN 1
        WHEN '1-3 Days Late' THEN 2
        WHEN '4-7 Days Late' THEN 3
        WHEN '8-14 Days Late' THEN 4
        WHEN '15+ Days Late' THEN 5
    END;


-- ============================================================
-- 3. STATE-LEVEL FULFILLMENT PERFORMANCE
-- ============================================================

SELECT
    customer_state,

    COUNT(*) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_late = 1
    ) AS late_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(delivery_delay_days)::numeric,
        2
    ) AS avg_delay_days,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(freight_ratio)::numeric,
        4
    ) AS avg_freight_ratio,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM analytics.order_analytics

WHERE is_delivered = 1

GROUP BY customer_state

HAVING COUNT(*) >= 50

ORDER BY
    late_delivery_rate DESC;


-- ============================================================
-- 4. SELLER-LEVEL FULFILLMENT PERFORMANCE
-- ============================================================
-- Seller information exists at order-item level.
-- Delivery/review metrics exist at order level.
-- Therefore we join the two analytical tables.
--
-- Freight is calculated as total seller freight / distinct
-- seller orders to avoid item-level duplication effects.
-- ============================================================

WITH seller_orders AS (
    SELECT
        oi.seller_id,
        oi.seller_state,
        oa.order_id,
        oa.delivery_days,
        oa.delivery_delay_days,
        oa.is_late,
        oa.review_score,
        SUM(oi.freight_value) AS order_freight

    FROM analytics.order_item_analytics oi

    JOIN analytics.order_analytics oa
        ON oi.order_id = oa.order_id

    WHERE oa.is_delivered = 1

    GROUP BY
        oi.seller_id,
        oi.seller_state,
        oa.order_id,
        oa.delivery_days,
        oa.delivery_delay_days,
        oa.is_late,
        oa.review_score
)

SELECT
    seller_id,
    seller_state,

    COUNT(*) AS orders,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(delivery_delay_days)::numeric,
        2
    ) AS avg_delay_days,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(order_freight)::numeric,
        2
    ) AS avg_freight_per_order,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM seller_orders

GROUP BY
    seller_id,
    seller_state

HAVING COUNT(*) >= 20

ORDER BY
    late_delivery_rate DESC

LIMIT 20;


-- ============================================================
-- 5. FREIGHT COST BY ORDER VALUE BAND
-- ============================================================

WITH order_bands AS (
    SELECT
        order_id,
        order_value,
        freight_cost,

        CASE
            WHEN order_value < 50
                THEN '<50'

            WHEN order_value < 100
                THEN '50-100'

            WHEN order_value < 250
                THEN '100-250'

            WHEN order_value < 500
                THEN '250-500'

            ELSE '500+'
        END AS order_value_band

    FROM analytics.order_analytics
)

SELECT
    order_value_band,

    COUNT(*) AS orders,

    ROUND(
        AVG(order_value)::numeric,
        2
    ) AS avg_order_value,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(
            freight_cost / NULLIF(order_value, 0)
        )::numeric,
        4
    ) AS avg_freight_ratio

FROM order_bands

GROUP BY order_value_band

ORDER BY
    CASE order_value_band
        WHEN '<50' THEN 1
        WHEN '50-100' THEN 2
        WHEN '100-250' THEN 3
        WHEN '250-500' THEN 4
        WHEN '500+' THEN 5
    END;


-- ============================================================
-- 6. FULFILLMENT RISK SEGMENTATION
-- ============================================================
-- Risk classification based on:
--   - Late delivery
--   - Long delivery duration
--   - High freight ratio
--
-- This is an analytical risk indicator, not a causal model.
-- ============================================================

WITH risk_data AS (
    SELECT
        order_id,
        delivery_days,
        freight_cost,
        freight_ratio,
        review_score,

        CASE
            WHEN
                is_late = 1
                OR delivery_days > 20
                OR freight_ratio > 0.50
            THEN 'High'

            WHEN
                delivery_days > 10
                OR freight_ratio > 0.30
                OR is_late = 1
            THEN 'Medium'

            ELSE 'Normal'
        END AS fulfillment_risk

    FROM analytics.order_analytics

    WHERE is_delivered = 1
)

SELECT
    fulfillment_risk,

    COUNT(*) AS orders,

    ROUND(
        100.0 * COUNT(*)
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_orders,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM risk_data

GROUP BY fulfillment_risk

ORDER BY
    CASE fulfillment_risk
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Normal' THEN 3
    END;


-- ============================================================
-- 7. DELIVERY PERFORMANCE VS CUSTOMER SATISFACTION
-- ============================================================

SELECT
    CASE
        WHEN is_late = 1
            THEN 'Late Delivery'
        ELSE 'On-Time / Early'
    END AS delivery_status,

    COUNT(*) AS orders,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE review_score <= 2
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS low_satisfaction_rate

FROM analytics.order_analytics

WHERE
    is_delivered = 1
    AND review_score IS NOT NULL

GROUP BY
    CASE
        WHEN is_late = 1
            THEN 'Late Delivery'
        ELSE 'On-Time / Early'
    END

ORDER BY
    delivery_status;


-- ============================================================
-- 8. HIGH-RISK ORDERS BY STATE
-- ============================================================

WITH risk_data AS (
    SELECT
        customer_state,
        order_id,
        delivery_days,
        freight_cost,
        freight_ratio,
        review_score,

        CASE
            WHEN
                is_late = 1
                OR delivery_days > 20
                OR freight_ratio > 0.50
            THEN 1
            ELSE 0
        END AS is_high_risk

    FROM analytics.order_analytics

    WHERE is_delivered = 1
)

SELECT
    customer_state,

    COUNT(*) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_high_risk = 1
    ) AS high_risk_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_high_risk = 1
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS high_risk_rate,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM risk_data

GROUP BY customer_state

HAVING COUNT(*) >= 50

ORDER BY
    high_risk_rate DESC;


-- ============================================================
-- 9. MONTHLY FULFILLMENT TREND
-- ============================================================

SELECT
    DATE_TRUNC(
        'month',
        order_purchase_timestamp
    ) AS order_month,

    COUNT(*) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_late = 1
    ) AS late_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM analytics.order_analytics

WHERE is_delivered = 1

GROUP BY
    DATE_TRUNC(
        'month',
        order_purchase_timestamp
    )

ORDER BY
    order_month;


-- ============================================================
-- 10. FULFILLMENT KPI SUMMARY
-- ============================================================
-- Compact summary for Power BI / reporting reference.
-- ============================================================

SELECT
    COUNT(*) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE is_late = 1
    ) AS late_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate,

    ROUND(
        AVG(delivery_days)::numeric,
        2
    ) AS avg_delivery_days,

    ROUND(
        AVG(freight_cost)::numeric,
        2
    ) AS avg_freight_cost,

    ROUND(
        AVG(freight_ratio)::numeric,
        4
    ) AS avg_freight_ratio,

    ROUND(
        AVG(review_score)::numeric,
        2
    ) AS avg_review_score

FROM analytics.order_analytics

WHERE is_delivered = 1;


-- ============================================================
-- END OF FULFILLMENT ANALYSIS
-- ============================================================