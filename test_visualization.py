from app.services.sql_service import execute_sql
from app.services.visualization_service import create_visualization


SQL = """
SELECT
    p.category,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - oi.discount / 100.0)
    ) AS revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY revenue DESC;
"""


print("=" * 60)
print("MILESTONE 8.6 - VISUALIZATION TEST")
print("=" * 60)


# ------------------------------------------------------------
# Execute SQL
# ------------------------------------------------------------

print("\n1. Executing SQL...")

df = execute_sql(SQL)

print("SQL executed successfully.")


# ------------------------------------------------------------
# Display data
# ------------------------------------------------------------

print("\n2. Query Result:")
print(df.to_string(index=False))


# ------------------------------------------------------------
# Create visualization recommendation
# ------------------------------------------------------------

print("\n3. Creating visualization recommendation...")

visualization = create_visualization(df)


print("\n4. Visualization Recommendation:")
print("TYPE:", visualization["type"])
print("REASON:", visualization["reason"])


print("\n" + "=" * 60)
print("MILESTONE 8.6 TEST COMPLETED")
print("=" * 60)