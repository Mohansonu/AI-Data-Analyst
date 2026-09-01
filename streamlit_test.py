import streamlit as st

from app.services.sql_service import execute_sql

st.set_page_config(page_title="SQL Test")

st.title("SQL Rendering Test")

if st.button("Run SQL"):

    result = execute_sql(
        "SELECT COUNT(*) AS total_customers FROM customers"
    )

    st.success("SQL executed")

    # DO NOT use st.dataframe()
    # DO NOT use st.table()

    value = result.iloc[0]["total_customers"]

    st.write("Result value:")
    st.write(value)

    st.metric(
        "Total Customers",
        str(value)
    )