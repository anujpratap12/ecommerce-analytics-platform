SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(AVG(order_total_value)::numeric, 2) AS average_order_value
FROM analytics.order_analytics
WHERE customer_state IS NOT NULL
GROUP BY customer_state
HAVING COUNT(DISTINCT order_id) >= 100
ORDER BY order_count DESC
LIMIT 10;