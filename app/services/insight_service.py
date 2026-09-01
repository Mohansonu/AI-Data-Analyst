import os
import json

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GENERATE BUSINESS INSIGHTS
# ============================================================

def generate_insights(
    question: str,
    sql: str,
    result
) -> dict:

    # Convert DataFrame into JSON-compatible records
    result_json = result.to_dict(
        orient="records"
    )

    prompt = f"""
You are a senior business data analyst working inside an
AI-powered business intelligence application.

Analyze the user's business question using ONLY the SQL
query result provided below.

============================================================
USER QUESTION
============================================================

{question}


============================================================
SQL QUERY
============================================================

{sql}


============================================================
QUERY RESULT
============================================================

{json.dumps(result_json, default=str)}


============================================================
ANALYSIS RULES
============================================================

1. Never invent numbers, facts, trends, or causes.

2. Use ONLY information available in the QUERY RESULT.

3. Do not assume the currency.

4. Do not add currency symbols such as $, €, or ₹ unless
   the currency is explicitly known from the data.

5. Format large numbers with commas when appropriate.

6. Keep the language clear and professional.

7. Avoid unnecessary technical terminology.

8. Do not repeat the SQL query in the findings.

9. Recommendations must be directly connected to the
   available data.

10. Do not claim that something caused a result unless the
    provided data proves it.

11. If the available result is insufficient to make a strong
    recommendation, clearly state that additional data is
    required.

12. Make sure words are separated correctly.

13. Never produce merged words such as:
    "holdtwo"
    "preventstockouts"

14. Do not mention information that is not present in the
    query result.

15. Keep the analysis concise and useful for a business user.


============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "2-3 sentence business summary",

    "key_findings": [
        "Clear finding based directly on the data",
        "Another important finding",
        "Another useful finding"
    ],

    "recommendations": [
        "Practical recommendation supported by the data",
        "Another practical recommendation",
        "Another recommendation or state that additional data is required"
    ]
}}

Do not include Markdown.
Do not include ```json.
Do not include any explanation outside the JSON.
"""


    # ========================================================
    # GEMINI REQUEST
    # ========================================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )


    # ========================================================
    # CHECK RESPONSE
    # ========================================================

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    text = response.text.strip()


    # ========================================================
    # REMOVE MARKDOWN CODE BLOCK IF PRESENT
    # ========================================================

    if text.startswith("```json"):

        text = text[7:]


    elif text.startswith("```"):

        text = text[3:]


    if text.endswith("```"):

        text = text[:-3]


    text = text.strip()


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        insights = json.loads(text)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}\n\n"
            f"Response:\n{text}"
        )


    # ========================================================
    # VALIDATE STRUCTURE
    # ========================================================

    required_keys = [
        "summary",
        "key_findings",
        "recommendations"
    ]

    for key in required_keys:

        if key not in insights:

            raise RuntimeError(
                f"Missing key in AI response: {key}"
            )


    return insights