from app.agents.sql_agent import generate_sql
from app.services.sql_validator import validate_sql
from app.services.sql_service import execute_sql


def ask_data_analyst(question: str):

    # ========================================================
    # STEP 1 — GENERATE SQL
    # ========================================================

    sql = generate_sql(question)


    # ========================================================
    # STEP 2 — VALIDATE SQL
    # ========================================================

    is_valid, message = validate_sql(sql)

    if not is_valid:

        raise ValueError(
            f"Generated SQL was blocked: {message}"
        )


    # ========================================================
    # STEP 3 — EXECUTE SQL
    # ========================================================

    result = execute_sql(sql)


    # ========================================================
    # STEP 4 — RETURN EVERYTHING
    # ========================================================

    return {
        "question": question,
        "sql": sql,
        "result": result
    }