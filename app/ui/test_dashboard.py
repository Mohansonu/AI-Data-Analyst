import streamlit as st

from app.ui.sql_playground import show_sql_playground


st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


st.title("📊 AI Data Analyst")

st.markdown(
    """
    ### AI-powered Business Intelligence Platform

    Ask questions about your business data,
    generate SQL, analyze results and receive
    business recommendations.
    """
)


show_sql_playground()