import streamlit as st

from app.services.sql_service import execute_sql


st.set_page_config(
    page_title="AI Data Analyst - SQL",
    page_icon="🔍"
)

st.title("📊 AI Data Analyst")

st.write("Application loaded successfully.")

st.divider()

st.subheader("🔍 SQL Query Playground")

query = st.text_area(
    "Enter SQL",
    value="SELECT COUNT(*) AS total_customers FROM customers;",
    height=150
)

if st.button("▶ Run SQL", type="primary"):

    st.write("1️⃣ Button clicked")

    try:

        result = execute_sql(query)

        st.write("2️⃣ SQL completed")

        st.write(
            "3️⃣ Result shape:",
            result.shape
        )

        st.write(
            "4️⃣ Columns:",
            list(result.columns)
        )

        if result.empty:

            st.warning("Query returned 0 rows.")

        else:

            st.success("5️⃣ Result received")

            # DON'T use dataframe/table
            for column in result.columns:

                value = result.iloc[0][column]

                st.metric(
                    str(column),
                    str(value)
                )

            st.write("6️⃣ Raw result:")

            st.write(
                result.to_dict(orient="records")
            )

    except Exception as error:

        st.error("SQL failed")

        st.exception(error)