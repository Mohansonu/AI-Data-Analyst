import streamlit as st


def render_sql_result(result):

    if result is None:

        st.warning("No result returned.")

        return


    if result.empty:

        st.info("Query executed successfully, but returned 0 rows.")

        return


    # ========================================================
    # RESULT INFORMATION
    # ========================================================

    rows = result.shape[0]
    columns = result.shape[1]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Rows",
            f"{rows:,}"
        )

    with col2:

        st.metric(
            "Columns",
            f"{columns:,}"
        )


    st.divider()

    st.subheader("📊 Query Result")


    # ========================================================
    # SINGLE VALUE
    # ========================================================

    if rows == 1 and columns == 1:

        column_name = str(result.columns[0])

        value = result.iloc[0, 0]

        st.metric(
            column_name.replace("_", " ").title(),
            str(value)
        )

        return


    # ========================================================
    # MULTIPLE RESULTS
    # ========================================================

    records = result.to_dict(
        orient="records"
    )


    for row_number, record in enumerate(
        records,
        start=1
    ):

        with st.expander(
            f"Row {row_number}"
        ):

            for column, value in record.items():

                st.write(
                    f"**{column}:** {value}"
                )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    csv_data = result.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="sql_result.csv",
        mime="text/csv"
    )