import streamlit as st
import pandas as pd

from app.services.ai_analyst_service import ask_data_analyst
from app.services.insight_service import generate_insights
from app.services.visualization_service import create_visualization
from app.services.chart_service import render_chart
from app.services.export_service import (
    dataframe_to_csv,
    dataframe_to_excel,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       FONT
       ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap'
    );


    /* ========================================================
       GLOBAL
       ======================================================== */

    html,
    body,
    [class*="css"],
    .stApp,
    input,
    textarea,
    button {

        font-family: "Inter", sans-serif !important;

    }


    .stApp {

        background: #f6f8fb;

        color: #172033;

    }


    .main .block-container {

        max-width: 1450px;

        padding-top: 1.2rem;

        padding-bottom: 3rem;

        padding-left: 3rem;

        padding-right: 3rem;

    }


    /* ========================================================
       REMOVE TOP STREAMLIT WHITE BAR
       ======================================================== */

    header[data-testid="stHeader"] {

        background: transparent !important;

        height: 0 !important;

        display: none !important;

    }


    div[data-testid="stDecoration"] {

        display: none !important;

    }


    div[data-testid="stToolbar"] {

        display: none !important;

    }


    #MainMenu {

        visibility: hidden;

    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background: #111827 !important;

        border-right: none !important;

    }


    section[data-testid="stSidebar"] > div {

        padding-top: 1.2rem;

    }


    .sidebar-title {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 22px;

        font-weight: 700;

        letter-spacing: -0.6px;

        color: #ffffff;

        line-height: 1.2;

    }


    .sidebar-subtitle {

        font-size: 12px;

        color: #9ca3af;

        margin-top: 5px;

    }


    .sidebar-section {

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 1.2px;

        text-transform: uppercase;

        color: #9ca3af;

        margin-top: 25px;

        margin-bottom: 9px;

    }


    .sidebar-description {

        color: #c4c9d2;

        font-size: 13px;

        line-height: 1.65;

    }


    .sidebar-status {

        background: #1f2937;

        border: 1px solid #374151;

        border-radius: 10px;

        padding: 10px 12px;

        margin-top: 14px;

        color: #d1d5db;

        font-size: 12px;

    }


    .sidebar-item {

        color: #c4c9d2;

        font-size: 12px;

        margin: 9px 0;

    }


    .sidebar-tip {

        color: #9ca3af;

        font-size: 12px;

        line-height: 1.6;

    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-badge {

        display: inline-block;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 1.5px;

        color: #4f46e5;

        background: #eef0ff;

        border: 1px solid #dfe2ff;

        border-radius: 20px;

        padding: 6px 11px;

        margin-bottom: 12px;

        animation: fadeUp 0.5s ease-out;

    }


    .hero-title {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: clamp(36px, 4vw, 50px);

        font-weight: 700;

        letter-spacing: -2px;

        line-height: 1.05;

        color: #111827;

        animation: fadeUp 0.65s ease-out;

    }


    .hero-subtitle {

        max-width: 820px;

        font-size: 15px;

        line-height: 1.7;

        color: #6b7280;

        margin-top: 12px;

        margin-bottom: 30px;

        animation: fadeUp 0.8s ease-out;

    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 21px;

        font-weight: 700;

        letter-spacing: -0.6px;

        color: #111827;

    }


    .section-description {

        font-size: 13px;

        color: #6b7280;

        margin-top: 3px;

        margin-bottom: 14px;

    }


    /* ========================================================
       SEARCH BAR
       ======================================================== */

    div[data-testid="stTextInput"] {

        margin-top: 4px;

    }


    div[data-testid="stTextInput"] input {

        height: 52px !important;

        min-height: 52px !important;

        border-radius: 12px !important;

        border: 1px solid #d9dee7 !important;

        background: #ffffff !important;

        color: #172033 !important;

        font-size: 14px !important;

        padding-left: 16px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease,
            transform 0.2s ease;

    }


    div[data-testid="stTextInput"] input::placeholder {

        color: #9aa2b1 !important;

    }


    div[data-testid="stTextInput"] input:focus {

        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 3px rgba(99, 102, 241, 0.09) !important;

        transform: translateY(-1px);

    }


    /* ========================================================
       EXAMPLES
       ======================================================== */

    .example-label {

        font-size: 11px;

        font-weight: 600;

        color: #7b8494;

        margin-top: 14px;

        margin-bottom: 7px;

    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        border-radius: 10px !important;

        min-height: 42px !important;

        font-family: "Inter", sans-serif !important;

        font-size: 13px !important;

        font-weight: 600 !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;

    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 7px 18px rgba(15, 23, 42, 0.08);

    }


    /* ========================================================
       ANALYSIS RESULT HEADER
       ======================================================== */

    .result-title {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 30px;

        font-weight: 700;

        letter-spacing: -0.9px;

        color: #111827;

        margin-top: 24px;

        margin-bottom: 4px;

        animation: fadeUp 0.5s ease-out;

    }


    .result-subtitle {

        font-size: 13px;

        color: #7a8496;

        margin-bottom: 20px;

        animation: fadeUp 0.65s ease-out;

    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f8fafc
            ) !important;

        border: 1px solid #e3e7ee !important;

        border-radius: 15px !important;

        padding: 18px 19px !important;

        min-height: 105px;

        box-shadow:
            0 4px 16px rgba(15, 23, 42, 0.045);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;

        animation: cardAppear 0.45s ease-out;

    }


    div[data-testid="stMetric"]:hover {

        transform: translateY(-4px);

        border-color: #d3d8e2 !important;

        box-shadow:
            0 12px 28px rgba(15, 23, 42, 0.08);

    }


    div[data-testid="stMetricLabel"] {

        font-size: 10px !important;

        font-weight: 700 !important;

        letter-spacing: 0.7px;

        text-transform: uppercase;

        color: #7b8494 !important;

    }


    div[data-testid="stMetricValue"] {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 27px !important;

        font-weight: 700 !important;

        letter-spacing: -0.8px;

        color: #111827 !important;

        margin-top: 5px;

    }


    /* ========================================================
       TABS
       ======================================================== */

    div[data-testid="stTabs"] {

        margin-top: 25px;

    }


    div[data-testid="stTabs"] button {

        font-size: 13px !important;

        font-weight: 600 !important;

        color: #7b8494 !important;

        padding: 10px 18px !important;

        transition:
            color 0.2s ease,
            transform 0.2s ease;

    }


    div[data-testid="stTabs"] button:hover {

        color: #111827 !important;

        transform: translateY(-1px);

    }


    div[data-testid="stTabs"]
    button[aria-selected="true"] {

        color: #111827 !important;

        font-weight: 700 !important;

    }


    div[data-testid="stTabs"]
    [data-baseweb="tab-highlight"] {

        background-color: #111827 !important;

        height: 2px !important;

    }


    /* ========================================================
       TAB TITLES
       ======================================================== */

    .tab-title {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 20px;

        font-weight: 700;

        color: #111827;

        letter-spacing: -0.5px;

        margin-top: 12px;

        margin-bottom: 4px;

    }


    .tab-description {

        font-size: 12px;

        color: #7b8494;

        margin-bottom: 18px;

    }


    /* ========================================================
       DATA TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border: 1px solid #e3e7ee;

        border-radius: 13px;

        overflow: hidden;

        background: #ffffff;

        box-shadow:
            0 4px 16px rgba(15, 23, 42, 0.035);

    }


    /* ========================================================
       SQL
       ======================================================== */

    div[data-testid="stCodeBlock"] {

        border-radius: 13px !important;

        border: 1px solid #252b38 !important;

        overflow: hidden;

        box-shadow:
            0 8px 22px rgba(15, 23, 42, 0.08);

    }


    /* ========================================================
       VISUALIZATION
       ======================================================== */

    div[data-testid="stPlotlyChart"] {

        background: #ffffff;

        border: 1px solid #e4e8ef;

        border-radius: 14px;

        padding: 8px;

        box-shadow:
            0 4px 16px rgba(15, 23, 42, 0.035);

        animation: cardAppear 0.55s ease-out;

    }


    /* ========================================================
       INSIGHTS
       ======================================================== */

    .insight-section-heading {

        font-family: "Space Grotesk", sans-serif !important;

        font-size: 18px;

        font-weight: 700;

        letter-spacing: -0.3px;

        color: #111827;

        margin-top: 22px;

        margin-bottom: 10px;

    }


    .finding-box {

        background: #ffffff;

        border: 1px solid #e5e8ee;

        border-radius: 12px;

        padding: 14px 17px;

        margin-bottom: 10px;

        font-size: 13px;

        line-height: 1.7;

        color: #596273;

        box-shadow:
            0 3px 10px rgba(15, 23, 42, 0.025);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;

        animation: cardAppear 0.4s ease-out;

    }


    .finding-box:hover {

        transform: translateY(-2px);

        box-shadow:
            0 8px 18px rgba(15, 23, 42, 0.055);

    }


    .summary-box {

        background: #ffffff;

        border: 1px solid #e5e8ee;

        border-radius: 14px;

        padding: 18px 20px;

        margin-bottom: 18px;

        font-size: 13px;

        line-height: 1.75;

        color: #596273;

        box-shadow:
            0 3px 12px rgba(15, 23, 42, 0.025);

        animation: cardAppear 0.45s ease-out;

    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px !important;

        font-size: 13px !important;

        line-height: 1.6 !important;

    }


    /* ========================================================
       DOWNLOAD BUTTON
       ======================================================== */

    div[data-testid="stDownloadButton"] button {

        border-radius: 10px !important;

        font-size: 13px !important;

        font-weight: 600 !important;

        min-height: 42px !important;

    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border: none !important;

        border-top: 1px solid #e5e7eb !important;

        margin-top: 22px !important;

        margin-bottom: 22px !important;

    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        text-align: center;

        font-size: 11px;

        color: #9aa2b1;

        padding-top: 35px;

    }


    /* ========================================================
       ANIMATIONS
       ======================================================== */

    @keyframes fadeUp {

        from {

            opacity: 0;

            transform: translateY(10px);

        }

        to {

            opacity: 1;

            transform: translateY(0);

        }

    }


    @keyframes cardAppear {

        from {

            opacity: 0;

            transform: translateY(8px);

        }

        to {

            opacity: 1;

            transform: translateY(0);

        }

    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .main .block-container {

            padding-left: 1.2rem;

            padding-right: 1.2rem;

        }

        .hero-title {

            font-size: 36px;

        }

        .result-title {

            font-size: 25px;

        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:

    st.session_state.analysis_result = None


if "question" not in st.session_state:

    st.session_state.question = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            📊 AI Data Analyst
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-subtitle">
            Intelligent business analytics
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    st.markdown(
        """
        <div class="sidebar-section">
            Platform
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-description">
            Ask questions about your PostgreSQL
            business data using natural language.
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-status">
            🟢 &nbsp; AI Analyst Ready
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-section">
            Capabilities
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-item">
            🤖 Natural Language → SQL
        </div>

        <div class="sidebar-item">
            🛡️ SQL Validation
        </div>

        <div class="sidebar-item">
            🐘 PostgreSQL Execution
        </div>

        <div class="sidebar-item">
            📊 Smart Visualization
        </div>

        <div class="sidebar-item">
            💡 AI Business Insights
        </div>

        <div class="sidebar-item">
            📄 CSV / Excel Export
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-section">
            Tip
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-tip">
            Ask specific business questions for
            more accurate analysis and useful insights.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-badge">
        AI-POWERED BUSINESS INTELLIGENCE
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero-title">
        Ask your data anything.
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero-subtitle">
        Turn natural-language business questions into SQL,
        interactive visualizations, and actionable insights.
        No manual SQL required.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ASK DATA ANALYST
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🤖 Ask Your Data Analyst
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="section-description">
        Enter a business question and let AI analyze your data.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SEARCH BAR
# ============================================================

question = st.text_input(
    "Business question",
    value=st.session_state.question,
    placeholder=(
        "Ask something like: "
        "What are the top 5 products by revenue?"
    ),
    label_visibility="collapsed",
)


# ============================================================
# EXAMPLES
# ============================================================

st.markdown(
    """
    <div class="example-label">
        Try asking
    </div>
    """,
    unsafe_allow_html=True,
)


example_col1, example_col2, example_col3, example_col4 = (
    st.columns(4)
)


examples = [
    "Show monthly revenue",
    "Top 5 products by revenue",
    "Revenue by category",
    "How many customers are there?",
]


example_columns = [
    example_col1,
    example_col2,
    example_col3,
    example_col4,
]


for column, example in zip(
    example_columns,
    examples,
):

    with column:

        if st.button(
            example,
            key=f"example_{example}",
            use_container_width=True,
        ):

            st.session_state.question = example

            st.rerun()


# ============================================================
# ACTION BUTTONS
# ============================================================

st.markdown("")


action_col1, action_col2 = st.columns(
    [4, 1]
)


with action_col1:

    analyze_clicked = st.button(
        "🚀 Analyze with AI",
        type="primary",
        use_container_width=True,
    )


with action_col2:

    clear_clicked = st.button(
        "↻ Clear",
        use_container_width=True,
    )


# ============================================================
# CLEAR
# ============================================================

if clear_clicked:

    st.session_state.question = ""

    st.session_state.analysis_result = None

    st.rerun()


# ============================================================
# AI ANALYSIS
# ============================================================

if analyze_clicked:

    if not question.strip():

        st.warning(
            "Please enter a business question before "
            "starting the analysis."
        )

        st.stop()


    try:

        with st.spinner(
            "🤖 AI is generating and executing SQL..."
        ):

            result = ask_data_analyst(
                question
            )


        st.session_state.analysis_result = result

        st.session_state.question = question

        st.rerun()


    except Exception as error:

        error_text = str(error)


        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            st.error(
                "⚠️ Gemini API quota has been exceeded."
            )

            st.info(
                "Please try again after the Gemini "
                "quota becomes available."
            )


        elif "503" in error_text:

            st.error(
                "⚠️ Gemini is temporarily unavailable."
            )

            st.info(
                "Please try again in a few moments."
            )


        else:

            st.error(
                f"❌ Analysis failed: {error}"
            )


        with st.expander(
            "🔧 Technical Error Details"
        ):

            st.exception(error)


# ============================================================
# ANALYSIS RESULTS
# ============================================================

if st.session_state.analysis_result is not None:

    result = st.session_state.analysis_result

    sql = result["sql"]

    dataframe = result["result"]


    # ========================================================
    # RESULT HEADER
    # ========================================================
    #
    # IMPORTANT:
    # This is deliberately rendered WITHOUT HTML.
    #
    # This fixes the issue where:
    #
    # <div class="result-title">
    #
    # was appearing directly on the screen.
    #
    # ========================================================

    st.markdown(
        "## 📊 Analysis Results"
    )

    st.caption(
        "AI-generated SQL, data visualization, "
        "and business intelligence."
    )


    # ========================================================
    # EMPTY RESULT
    # ========================================================

    if dataframe is None or dataframe.empty:

        st.info(
            "The query executed successfully, "
            "but returned no results."
        )

        st.stop()


    # ========================================================
    # BASIC KPIs
    # ========================================================

    numeric_columns = (
        dataframe
        .select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )


    metric_col1, metric_col2, metric_col3 = (
        st.columns(3)
    )


    with metric_col1:

        st.metric(
            "Rows Returned",
            f"{len(dataframe):,}",
        )


    with metric_col2:

        st.metric(
            "Columns",
            f"{len(dataframe.columns):,}",
        )


    with metric_col3:

        st.metric(
            "Numeric Fields",
            f"{len(numeric_columns):,}",
        )


    # ========================================================
    # RESULT TABS
    # ========================================================

    tab_data, tab_visualization, tab_sql, tab_insights = (
        st.tabs(
            [
                "📊 Data",
                "📈 Visualization",
                "🧠 SQL",
                "💡 AI Insights",
            ]
        )
    )


    # ========================================================
    # DATA TAB
    # ========================================================

    with tab_data:

        st.markdown(
            "### 📊 Query Result"
        )

        st.caption(
            "Explore the records returned from your "
            "business question."
        )


        st.dataframe(
            dataframe,
            use_container_width=True,
            height=430,
        )


        st.caption(
            f"{len(dataframe):,} rows × "
            f"{len(dataframe.columns):,} columns"
        )


        st.markdown(
            "### ⬇️ Export Results"
        )


        st.caption(
            "Download the analyzed data for further use."
        )


        export_col1, export_col2 = (
            st.columns(2)
        )


        with export_col1:

            csv_data = dataframe_to_csv(
                dataframe
            )


            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name="ai_data_analyst_results.csv",
                mime="text/csv",
                use_container_width=True,
            )


        with export_col2:

            excel_data = dataframe_to_excel(
                dataframe
            )


            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name="ai_data_analyst_results.xlsx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True,
            )


    # ========================================================
    # VISUALIZATION TAB
    # ========================================================

    with tab_visualization:

        st.markdown(
            "### 📈 Data Visualization"
        )


        st.caption(
            "The most suitable visualization has been "
            "selected automatically based on your data."
        )


        visualization = create_visualization(
            dataframe
        )


        chart_type = visualization.get(
            "type",
            "table",
        )


        reason = visualization.get(
            "reason",
            "Visualization selected automatically.",
        )


        info_col1, info_col2 = (
            st.columns(2)
        )


        with info_col1:

            st.metric(
                "Recommended Chart",
                chart_type.upper(),
            )


        with info_col2:

            st.markdown(
                "#### Why this visualization?"
            )


            st.write(
                reason
            )


        # ====================================================
        # CHART
        # ====================================================

        if chart_type in (
            "bar",
            "line",
            "scatter",
            "area",
            "histogram",
            "pie",
            "donut",
            "horizontal_bar",
            "multi_line",
            "heatmap",
            "map",
        ):

            chart = render_chart(
                dataframe,
                visualization,
            )


            if chart is not None:

                st.plotly_chart(
                    chart,
                    use_container_width=True,
                )


            else:

                st.warning(
                    "The recommended visualization "
                    "could not be rendered."
                )


        # ====================================================
        # METRIC
        # ====================================================

        elif chart_type == "metric":

            value_column = visualization.get(
                "value"
            )


            if (
                value_column
                and value_column in dataframe.columns
            ):

                value = dataframe[
                    value_column
                ].iloc[0]


                st.metric(
                    label=(
                        str(value_column)
                        .replace(
                            "_",
                            " ",
                        )
                        .title()
                    ),
                    value=f"{value:,.2f}",
                )


            else:

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                )


        # ====================================================
        # KPI CARDS
        # ====================================================

        elif chart_type == "kpi_cards":

            numeric_columns = (
                dataframe
                .select_dtypes(
                    include="number"
                )
                .columns
                .tolist()
            )


            if numeric_columns:

                columns = st.columns(
                    min(
                        len(numeric_columns),
                        4,
                    )
                )


                for index, column in enumerate(
                    numeric_columns[:4]
                ):

                    value = dataframe[
                        column
                    ].iloc[0]


                    with columns[index]:

                        st.metric(
                            str(column)
                            .replace(
                                "_",
                                " ",
                            )
                            .title(),

                            f"{value:,.2f}",
                        )


            else:

                st.dataframe(
                    dataframe,
                    use_container_width=True,
                )


        # ====================================================
        # TABLE
        # ====================================================

        else:

            st.info(
                "This result is best represented as a table."
            )


            st.dataframe(
                dataframe,
                use_container_width=True,
            )


    # ========================================================
    # SQL TAB
    # ========================================================

    with tab_sql:

        st.markdown(
            "### 🧠 Generated SQL"
        )


        st.caption(
            "SQL generated from your natural-language "
            "business question."
        )


        st.code(
            sql,
            language="sql",
        )


    # ========================================================
    # AI INSIGHTS TAB
    # ========================================================

    with tab_insights:

        st.markdown(
            "### 💡 AI Business Insights"
        )


        st.caption(
            "Understand what your data means and "
            "what actions you can take."
        )


        try:

            with st.spinner(
                "🤖 Generating business insights..."
            ):

                insights = generate_insights(
                    result["question"],
                    result["sql"],
                    result["result"],
                )


            # =================================================
            # SUMMARY
            # =================================================

            st.markdown(
                "#### 📌 Summary"
            )


            summary = insights.get(
                "summary",
                "No summary was generated.",
            )


            # -------------------------------------------------
            # IMPORTANT:
            #
            # AI-generated content is NOT placed inside:
            #
            # <div class="insight-text">
            #
            # Instead we use Streamlit directly.
            # -------------------------------------------------

            st.markdown(
                str(summary)
            )


            # =================================================
            # KEY FINDINGS
            # =================================================

            st.markdown(
                "#### 🔎 Key Findings"
            )


            findings = insights.get(
                "key_findings",
                [],
            )


            if findings:

                for finding in findings:

                    st.markdown(
                        f"- {str(finding)}"
                    )

            else:

                st.info(
                    "No key findings were generated."
                )


            # =================================================
            # RECOMMENDATIONS
            # =================================================

            st.markdown(
                "#### 🎯 Recommendations"
            )


            recommendations = insights.get(
                "recommendations",
                [],
            )


            if recommendations:

                for recommendation in recommendations:

                    st.markdown(
                        f"- {str(recommendation)}"
                    )

            else:

                st.info(
                    "No recommendations were generated."
                )


            st.success(
                "✅ AI analysis completed successfully!"
            )


        except Exception as error:

            error_text = str(error)


            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "quota" in error_text.lower()
            ):

                st.error(
                    "⚠️ Gemini API quota has been exceeded "
                    "while generating insights."
                )


                st.info(
                    "The SQL query and data results are still "
                    "available in the other tabs."
                )


            elif "503" in error_text:

                st.error(
                    "⚠️ Gemini is temporarily unavailable."
                )


                st.info(
                    "Please try again in a few moments."
                )


            else:

                st.error(
                    f"❌ Insight generation failed: {error}"
                )


            with st.expander(
                "🔧 Technical Error Details"
            ):

                st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Data Analyst
        • Natural Language Analytics
        • PostgreSQL
        • Gemini
    </div>
    """,
    unsafe_allow_html=True,
)