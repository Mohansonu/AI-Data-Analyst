import re


# ============================================================
# FORBIDDEN SQL OPERATIONS
# ============================================================

FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


# ============================================================
# VALIDATE SQL
# ============================================================

def validate_sql(sql: str) -> tuple[bool, str]:

    if not sql or not sql.strip():

        return False, "SQL query is empty."


    # Remove leading/trailing whitespace

    cleaned_sql = sql.strip()


    # Remove trailing semicolon

    cleaned_sql = cleaned_sql.rstrip(";").strip()


    # ========================================================
    # ONLY SELECT / WITH
    # ========================================================

    if not re.match(
        r"^(SELECT|WITH)\b",
        cleaned_sql,
        re.IGNORECASE
    ):

        return (
            False,
            "Only SELECT or WITH queries are allowed."
        )


    # ========================================================
    # BLOCK MULTIPLE STATEMENTS
    # ========================================================

    if ";" in cleaned_sql:

        return (
            False,
            "Multiple SQL statements are not allowed."
        )


    # ========================================================
    # BLOCK DANGEROUS KEYWORDS
    # ========================================================

    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            cleaned_sql,
            re.IGNORECASE
        ):

            return (
                False,
                f"Forbidden SQL operation detected: {keyword}"
            )


    # ========================================================
    # VALID
    # ========================================================

    return True, "SQL query is safe."