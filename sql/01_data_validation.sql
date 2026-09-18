-- ============================================================
-- E-COMMERCE ANALYTICS PLATFORM
-- SQL DATA VALIDATION
-- ============================================================


-- ============================================================
-- 1. CHECK CUSTOMER → ORDER RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS orders_without_customer
FROM staging.orders o
LEFT JOIN staging.customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- ============================================================
-- 2. CHECK ORDER → ORDER ITEM RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS orders_without_items
FROM staging.orders o
LEFT JOIN staging.order_items oi
    ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL;


-- ============================================================
-- 3. CHECK ORDER ITEM → PRODUCT RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS items_without_product
FROM staging.order_items oi
LEFT JOIN staging.products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- ============================================================
-- 4. CHECK ORDER ITEM → SELLER RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS items_without_seller
FROM staging.order_items oi
LEFT JOIN staging.sellers s
    ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;


-- ============================================================
-- 5. CHECK ORDER → PAYMENT RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS orders_without_payment
FROM staging.orders o
LEFT JOIN staging.payments p
    ON o.order_id = p.order_id
WHERE p.order_id IS NULL;


-- ============================================================
-- 6. CHECK ORDER → REVIEW RELATIONSHIP
-- ============================================================

SELECT COUNT(*) AS orders_without_review
FROM staging.orders o
LEFT JOIN staging.reviews r
    ON o.order_id = r.order_id
WHERE r.order_id IS NULL;


-- ============================================================
-- 7. CHECK DUPLICATE ORDER IDs
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS order_count
FROM staging.orders
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;


-- ============================================================
-- 8. CHECK DUPLICATE CUSTOMER IDs
-- ============================================================

SELECT
    customer_id,
    COUNT(*) AS customer_count
FROM staging.customers
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY customer_count DESC;


-- ============================================================
-- 9. CHECK INVALID REVIEW SCORES
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS review_count
FROM staging.reviews
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 10. CHECK NEGATIVE PRICES
-- ============================================================

SELECT COUNT(*) AS negative_prices
FROM staging.order_items
WHERE price < 0;


-- ============================================================
-- 11. CHECK NEGATIVE FREIGHT VALUES
-- ============================================================

SELECT COUNT(*) AS negative_freight
FROM staging.order_items
WHERE freight_value < 0;


-- ============================================================
-- 12. CHECK DELIVERY DATE LOGIC
-- ============================================================

SELECT COUNT(*) AS invalid_delivery_dates
FROM staging.orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_delivered_customer_date
      < order_purchase_timestamp;


-- ============================================================
-- 13. CHECK ESTIMATED DELIVERY DATE LOGIC
-- ============================================================

SELECT COUNT(*) AS invalid_estimated_dates
FROM staging.orders
WHERE order_estimated_delivery_date IS NOT NULL
  AND order_estimated_delivery_date
      < order_purchase_timestamp;


-- ============================================================
-- 14. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_orders
FROM staging.orders
GROUP BY order_status
ORDER BY order_count DESC;


-- ============================================================
-- 15. PAYMENT TYPE DISTRIBUTION
-- ============================================================

SELECT
    payment_type,
    COUNT(*) AS payment_count,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_payments
FROM staging.payments
GROUP BY payment_type
ORDER BY payment_count DESC;