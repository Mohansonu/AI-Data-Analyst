-- ============================================================
-- AI DATA ANALYST
-- MILESTONE 5 - SQL ANALYTICS ENGINE
-- ============================================================


-- ============================================================
-- 1. DATABASE OVERVIEW
-- ============================================================

SELECT
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM orders) AS total_orders,
    (SELECT COUNT(*) FROM order_items) AS total_order_items,
    (SELECT COUNT(*) FROM payments) AS total_payments;