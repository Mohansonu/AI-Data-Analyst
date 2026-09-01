import streamlit as st
from app.services.sql_service import execute_sql


def show_sql_playground():

    st.divider()

    st.header("🔍 SQL Query Playground")

    st.write("Enter a read-only SQL query and execute it.")

    query = st.text_area(
        "SQL Query",
        value="SELECT COUNT(*) AS total_customers FROM customers;",
        height=150,
        key="sql_input"
    )

    run = st.button(
        "▶ Run SQL",
        key="execute_sql"
    )

    if run:

        st.write("1️⃣ Button clicked")

        try:

            st.write("2️⃣ Executing SQL...")

            result = execute_sql(query)

            st.write("3️⃣ SQL execution completed")

            st.write(
                f"4️⃣ Rows returned: {len(result)}"
            )

            st.write(
                f"5️⃣ Columns returned: {len(result.columns)}"
            )

            st.write("6️⃣ Result:")

            # IMPORTANT:
            # Do NOT use st.dataframe here.
            # Render the result manually.

            if result.empty:

                st.warning(
                    "Query executed successfully, "
                    "but returned no rows."
                )

            else:

                for column in result.columns:

                    value = result.iloc[0][column]

                    st.metric(
                        str(column)
                        .replace("_", " ")
                        .title(),
                        str(value)
                    )

                st.write("7️⃣ Raw result:")

                st.json(
                    result.to_dict(
                        orient="records"
                    )
                )

        except Exception as error:

            st.error("❌ SQL execution failed")

            st.code(
                str(error)
            )