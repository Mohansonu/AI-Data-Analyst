import streamlit as st
import plotly.express as px

from app.services.analytics_service import (
    get_database_summary,
    get_revenue_by_category,
    get_monthly_revenue,
    get_top_products,
    get_revenue_by_state,
)

from app.ui.sql_playground import show_sql_playground


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 AI Data Analyst")

st.markdown(
    """
    ### Business Intelligence Dashboard

    Explore business performance using PostgreSQL analytics
    and interactive SQL.
    """
)


# ============================================================
# DATABASE OVERVIEW
# ============================================================

st.divider()

st.subheader("📌 Database Overview")


try:

    summary = get_database_summary()

    if not summary.empty:

        data = summary.iloc[0]

        col1, col2, col3, col4, col5 = st.columns(5)


        with col1:

            st.metric(
                "Customers",
                f"{int(data['total_customers']):,}"
            )


        with col2:

            st.metric(
                "Products",
                f"{int(data['total_products']):,}"
            )


        with col3:

            st.metric(
                "Orders",
                f"{int(data['total_orders']):,}"
            )


        with col4:

            st.metric(
                "Order Items",
                f"{int(data['total_order_items']):,}"
            )


        with col5:

            st.metric(
                "Payments",
                f"{int(data['total_payments']):,}"
            )


except Exception as error:

    st.error(
        f"Database summary failed: {error}"
    )


# ============================================================
# CATEGORY REVENUE
# ============================================================

st.divider()

st.subheader("💰 Revenue by Category")


try:

    category_data = get_revenue_by_category()


    if not category_data.empty:

        fig = px.bar(
            category_data,

            x="category",

            y="revenue",

            title="Revenue by Category",

            text_auto=".2s"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


except Exception as error:

    st.error(
        f"Category analysis failed: {error}"
    )


# ============================================================
# MONTHLY REVENUE
# ============================================================

st.divider()

st.subheader("📈 Monthly Revenue")


try:

    monthly_data = get_monthly_revenue()


    if not monthly_data.empty:

        fig = px.line(
            monthly_data,

            x="month",

            y="revenue",

            markers=True,

            title="Monthly Revenue Trend"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


except Exception as error:

    st.error(
        f"Monthly revenue failed: {error}"
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()

st.subheader("🏆 Top 10 Products")


try:

    top_products = get_top_products()


    if not top_products.empty:

        for index, row in top_products.iterrows():

            product = row["product_name"]

            units = row["units_sold"]

            revenue = row["revenue"]


            st.write(
                f"**{index + 1}. {product}**  "
                f"— {int(units):,} units  "
                f"— Revenue: ₹{float(revenue):,.2f}"
            )


except Exception as error:

    st.error(
        f"Top products failed: {error}"
    )


# ============================================================
# STATE REVENUE
# ============================================================

st.divider()

st.subheader("🌎 Revenue by State")


try:

    state_data = get_revenue_by_state()


    if not state_data.empty:

        fig = px.bar(
            state_data,

            x="state",

            y="revenue",

            title="Revenue by State",

            text_auto=".2s"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


except Exception as error:

    st.error(
        f"State analysis failed: {error}"
    )


# ============================================================
# SQL PLAYGROUND
# ============================================================

show_sql_playground()