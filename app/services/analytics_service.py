from app.services.sql_service import execute_sql


def get_database_summary():

    query = """
    SELECT

        (SELECT COUNT(*)
         FROM customers) AS total_customers,

        (SELECT COUNT(*)
         FROM products) AS total_products,

        (SELECT COUNT(*)
         FROM orders) AS total_orders,

        (SELECT COUNT(*)
         FROM order_items) AS total_order_items,

        (SELECT COUNT(*)
         FROM payments) AS total_payments;
    """

    return execute_sql(query)


def get_revenue_by_category():

    query = """
    SELECT

        p.category,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount / 100.0)
            ),
            2
        ) AS revenue

    FROM order_items oi

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    WHERE o.status = 'Completed'

    GROUP BY p.category

    ORDER BY revenue DESC;
    """

    return execute_sql(query)


def get_monthly_revenue():

    query = """
    SELECT

        DATE_TRUNC(
            'month',
            o.order_date
        ) AS month,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount / 100.0)
            ),
            2
        ) AS revenue

    FROM order_items oi

    JOIN orders o
        ON oi.order_id = o.order_id

    WHERE o.status = 'Completed'

    GROUP BY month

    ORDER BY month;
    """

    return execute_sql(query)


def get_top_products():

    query = """
    SELECT

        p.product_name,

        SUM(
            oi.quantity
        ) AS units_sold,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount / 100.0)
            ),
            2
        ) AS revenue

    FROM order_items oi

    JOIN products p
        ON oi.product_id = p.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    WHERE o.status = 'Completed'

    GROUP BY
        p.product_id,
        p.product_name

    ORDER BY revenue DESC

    LIMIT 10;
    """


    return execute_sql(query)


def get_revenue_by_state():

    query = """
    SELECT

        c.state,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount / 100.0)
            ),
            2
        ) AS revenue

    FROM order_items oi

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN customers c
        ON o.customer_id = c.customer_id

    WHERE o.status = 'Completed'

    GROUP BY c.state

    ORDER BY revenue DESC;
    """


    return execute_sql(query)