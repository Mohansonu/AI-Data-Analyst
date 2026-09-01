import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# DATABASE SCHEMA
# ============================================================

DATABASE_SCHEMA = """

PostgreSQL Database Schema

TABLE: customers

Columns:
- customer_id
- customer_name
- email
- phone
- city
- state
- signup_date


TABLE: products

Columns:
- product_id
- product_name
- category
- price
- stock


TABLE: orders

Columns:
- order_id
- customer_id
- order_date
- status
- total_amount


TABLE: order_items

Columns:
- order_item_id
- order_id
- product_id
- quantity
- unit_price
- discount


TABLE: payments

Columns:
- payment_id
- order_id
- payment_date
- payment_method
- amount
- payment_status

"""


# ============================================================
# AI INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTION = f"""

You are an expert PostgreSQL Data Analyst.

Your task is to convert a user's business question
into a valid PostgreSQL SELECT query.

{DATABASE_SCHEMA}

IMPORTANT RULES:

1. Return ONLY SQL.
2. Do not return markdown.
3. Do not return explanations.
4. Only SELECT and WITH queries are allowed.
5. Never use INSERT.
6. Never use UPDATE.
7. Never use DELETE.
8. Never use DROP.
9. Never use ALTER.
10. Never use TRUNCATE.
11. Never modify database data.
12. Use only tables and columns from the schema.
13. Use valid PostgreSQL syntax.

REVENUE CALCULATION:

For order_items, revenue should normally be calculated as:

quantity * unit_price * (1 - discount / 100.0)

COMPLETED ORDERS:

When analyzing actual sales revenue, normally use:

orders.status = 'Completed'

RANKINGS:

Use ORDER BY and LIMIT when the user asks for
top, highest, lowest, best, or worst results.

"""


# ============================================================
# GENERATE SQL
# ============================================================

def generate_sql(question: str) -> str:

    if not question or not question.strip():

        raise ValueError(
            "Question cannot be empty."
        )


    prompt = f"""
{SYSTEM_INSTRUCTION}

USER QUESTION:

{question}

Generate the PostgreSQL SQL query now.
"""


    # ========================================================
    # GEMINI 3.6 FLASH
    # ========================================================

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt
    )


    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    sql = response.text.strip()


    # ========================================================
    # REMOVE MARKDOWN CODE FENCES
    # ========================================================

    if sql.startswith("```sql"):

        sql = sql[6:]


    if sql.startswith("```"):

        sql = sql[3:]


    if sql.endswith("```"):

        sql = sql[:-3]


    return sql.strip()