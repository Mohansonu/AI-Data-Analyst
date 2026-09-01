import os
import random
from datetime import datetime, timedelta

import pandas as pd
import psycopg2
from faker import Faker
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "ai_data_analyst"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


# Number of records
NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 1_000
NUM_ORDERS = 50_000


fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)


# ============================================================
# BUSINESS DATA
# ============================================================

INDIAN_CITIES = [
    ("Hyderabad", "Telangana"),
    ("Warangal", "Telangana"),
    ("Bengaluru", "Karnataka"),
    ("Chennai", "Tamil Nadu"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Vijayawada", "Andhra Pradesh"),
    ("Kochi", "Kerala"),
    ("Coimbatore", "Tamil Nadu"),
    ("Bhopal", "Madhya Pradesh"),
]

CATEGORIES = {
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Tablets",
        "Headphones",
        "Monitors",
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Home Decor",
        "Appliances",
    ],
    "Fashion": [
        "Men Clothing",
        "Women Clothing",
        "Footwear",
        "Accessories",
    ],
    "Sports": [
        "Fitness",
        "Outdoor",
        "Cricket",
        "Football",
    ],
    "Books": [
        "Technology",
        "Fiction",
        "Business",
        "Education",
    ],
}

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
]

CUSTOMER_SEGMENTS = [
    "Premium",
    "Regular",
    "Occasional",
    "New",
]

ORDER_STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Pending",
    "Returned",
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers():

    customers = []

    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 12, 31)

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        city, state = random.choice(INDIAN_CITIES)

        registration_date = fake.date_between(
            start_date=start_date.date(),
            end_date=end_date.date()
        )

        customers.append({
            "customer_id": customer_id,
            "name": fake.name(),
            "email": f"customer{customer_id}@example.com",
            "city": city,
            "state": state,
            "country": "India",
            "registration_date": registration_date,
            "customer_segment": random.choices(
                CUSTOMER_SEGMENTS,
                weights=[15, 50, 25, 10]
            )[0],
        })

    return pd.DataFrame(customers)


# ============================================================
# GENERATE PRODUCTS
# ============================================================

def generate_products():

    products = []

    product_id = 1

    for category, subcategories in CATEGORIES.items():

        for _ in range(NUM_PRODUCTS // len(CATEGORIES)):

            subcategory = random.choice(subcategories)

            price = round(
                random.uniform(300, 150000),
                2
            )

            cost = round(
                price * random.uniform(0.55, 0.85),
                2
            )

            products.append({
                "product_id": product_id,
                "product_name": f"{subcategory} Product {product_id}",
                "category": category,
                "subcategory": subcategory,
                "price": price,
                "cost": cost,
            })

            product_id += 1

    return pd.DataFrame(products)


# ============================================================
# GENERATE ORDERS
# ============================================================

def generate_orders():

    orders = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    for order_id in range(1, NUM_ORDERS + 1):

        customer_id = random.randint(
            1,
            NUM_CUSTOMERS
        )

        order_date = fake.date_time_between(
            start_date=start_date,
            end_date=end_date
        )

        status = random.choice(ORDER_STATUSES)

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status,
            "total_amount": 0,
        })

    return pd.DataFrame(orders)


# ============================================================
# GENERATE ORDER ITEMS
# ============================================================

def generate_order_items(orders, products):

    order_items = []

    order_item_id = 1

    product_lookup = products.set_index("product_id")

    order_totals = {}

    for _, order in orders.iterrows():

        order_id = int(order["order_id"])

        number_of_items = random.randint(1, 5)

        selected_products = random.sample(
            list(products["product_id"]),
            number_of_items
        )

        total = 0

        for product_id in selected_products:

            product = product_lookup.loc[product_id]

            quantity = random.randint(1, 4)

            unit_price = float(product["price"])

            discount = round(
                random.uniform(0, 25),
                2
            )

            item_total = (
                quantity
                * unit_price
                * (1 - discount / 100)
            )

            total += item_total

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
            })

            order_item_id += 1

        order_totals[order_id] = round(total, 2)

    orders["total_amount"] = orders["order_id"].map(
        order_totals
    )

    return (
        pd.DataFrame(order_items),
        orders
    )


# ============================================================
# GENERATE PAYMENTS
# ============================================================

def generate_payments(orders):

    payments = []

    for _, order in orders.iterrows():

        order_id = int(order["order_id"])

        payment_status = (
            "Paid"
            if order["status"] == "Completed"
            else random.choice(
                ["Pending", "Failed", "Paid"]
            )
        )

        payments.append({
            "payment_id": order_id,
            "order_id": order_id,
            "payment_method": random.choice(
                PAYMENT_METHODS
            ),
            "payment_status": payment_status,
            "payment_date": order["order_date"],
        })

    return pd.DataFrame(payments)


# ============================================================
# INSERT DATA INTO POSTGRESQL
# ============================================================

def insert_dataframe(cursor, table_name, dataframe):

    columns = list(dataframe.columns)

    column_string = ", ".join(columns)

    placeholders = ", ".join(
        ["%s"] * len(columns)
    )

    query = f"""
        INSERT INTO {table_name}
        ({column_string})
        VALUES ({placeholders})
    """

    records = [
        tuple(row)
        for row in dataframe.itertuples(
            index=False,
            name=None
        )
    ]

    cursor.executemany(
        query,
        records
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("AI DATA ANALYST - DATABASE SEEDING")
    print("=" * 60)

    print("\nGenerating customers...")
    customers = generate_customers()

    print(
        f"Customers generated: {len(customers):,}"
    )

    print("\nGenerating products...")
    products = generate_products()

    print(
        f"Products generated: {len(products):,}"
    )

    print("\nGenerating orders...")
    orders = generate_orders()

    print(
        f"Orders generated: {len(orders):,}"
    )

    print("\nGenerating order items...")
    order_items, orders = generate_order_items(
        orders,
        products
    )

    print(
        f"Order items generated: "
        f"{len(order_items):,}"
    )

    print("\nGenerating payments...")
    payments = generate_payments(orders)

    print(
        f"Payments generated: {len(payments):,}"
    )

    # --------------------------------------------------------
    # Save CSV backups
    # --------------------------------------------------------

    print("\nSaving CSV files...")

    customers.to_csv(
        "data/customers.csv",
        index=False
    )

    products.to_csv(
        "data/products.csv",
        index=False
    )

    orders.to_csv(
        "data/orders.csv",
        index=False
    )

    order_items.to_csv(
        "data/order_items.csv",
        index=False
    )

    payments.to_csv(
        "data/payments.csv",
        index=False
    )

    print("CSV files created successfully.")

    # --------------------------------------------------------
    # Connect to PostgreSQL
    # --------------------------------------------------------

    print("\nConnecting to PostgreSQL...")

    connection = get_connection()

    cursor = connection.cursor()

    try:

        print("\nInserting customers...")
        insert_dataframe(
            cursor,
            "customers",
            customers
        )

        print("Inserting products...")
        insert_dataframe(
            cursor,
            "products",
            products
        )

        print("Inserting orders...")
        insert_dataframe(
            cursor,
            "orders",
            orders
        )

        print("Inserting order items...")
        insert_dataframe(
            cursor,
            "order_items",
            order_items
        )

        print("Inserting payments...")
        insert_dataframe(
            cursor,
            "payments",
            payments
        )

        connection.commit()

        print("\n" + "=" * 60)
        print("DATA INSERTION COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as error:

        connection.rollback()

        print("\nERROR:")
        print(error)

        raise

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()