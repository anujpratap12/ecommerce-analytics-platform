WITH validation_results AS (
    SELECT
        'Duplicate order_id values' AS validation,
        COALESCE(SUM(order_count - 1), 0)::bigint AS issue_count
    FROM (
        SELECT
            order_id,
            COUNT(*) AS order_count
        FROM analytics.order_analytics
        GROUP BY order_id
        HAVING COUNT(*) > 1
    ) duplicates

    UNION ALL

    SELECT
        'NULL customer_state values',
        COUNT(*)::bigint
    FROM analytics.order_analytics
    WHERE customer_state IS NULL

    UNION ALL

    SELECT
        'NULL order_total_value values',
        COUNT(*)::bigint
    FROM analytics.order_analytics
    WHERE order_total_value IS NULL

    UNION ALL

    SELECT
        'Negative order_total_value values',
        COUNT(*)::bigint
    FROM analytics.order_analytics
    WHERE order_total_value < 0
)
SELECT
    validation,
    issue_count,
    CASE
        WHEN issue_count = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM validation_results
ORDER BY validation;