import pandas as pd


# ============================================================
# HELPERS
# ============================================================

def _is_time_column(column_name: str) -> bool:
    """
    Detect whether a column name looks like a time/date field.
    """

    name = str(column_name).lower()

    time_keywords = [
        "date",
        "time",
        "month",
        "year",
        "week",
        "day",
        "quarter",
        "timestamp",
    ]

    return any(keyword in name for keyword in time_keywords)


def _is_geo_column(column_name: str) -> bool:
    """
    Detect geographic columns.
    """

    name = str(column_name).lower()

    geo_keywords = [
        "state",
        "city",
        "country",
        "region",
        "latitude",
        "longitude",
        "lat",
        "lon",
        "location",
    ]

    return any(keyword in name for keyword in geo_keywords)


def _looks_like_percentage(series: pd.Series) -> bool:
    """
    Detect whether a numeric column looks like percentage/proportion data.
    """

    if series.empty:
        return False

    try:
        values = pd.to_numeric(
            series,
            errors="coerce"
        ).dropna()

        if values.empty:
            return False

        return (
            values.min() >= 0
            and values.max() <= 100
        )

    except Exception:
        return False


# ============================================================
# MAIN VISUALIZATION RECOMMENDER
# ============================================================

def create_visualization(df: pd.DataFrame) -> dict:
    """
    Automatically recommend the most appropriate visualization
    based on the structure of a query result.

    Supported types:

    bar
    line
    area
    scatter
    histogram
    pie
    donut
    horizontal_bar
    multi_line
    heatmap
    map
    metric
    kpi_cards
    table
    none
    """

    # ========================================================
    # 1. EMPTY DATAFRAME
    # ========================================================

    if df is None or df.empty:

        return {
            "type": "none",
            "reason": (
                "The query returned no data, "
                "so no visualization is required."
            )
        }

    # ========================================================
    # 2. IDENTIFY COLUMN TYPES
    # ========================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=[
            "object",
            "category",
            "string"
        ]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=[
            "datetime",
            "datetimetz"
        ]).columns.tolist()

    time_columns = datetime_columns.copy()

    for column in categorical_columns:

        if _is_time_column(column):

            if column not in time_columns:
                time_columns.append(column)

    geo_columns = [
        column
        for column in df.columns
        if _is_geo_column(column)
    ]

    # ========================================================
    # 3. SINGLE VALUE
    # ========================================================

    if (
        len(df) == 1
        and len(numeric_columns) == 1
    ):

        return {
            "type": "metric",
            "value": numeric_columns[0],
            "reason": (
                "The result contains a single numeric KPI, "
                "so a metric card is appropriate."
            )
        }

    # ========================================================
    # 4. MULTIPLE KPIs
    # ========================================================

    if (
        len(df) == 1
        and len(numeric_columns) >= 2
    ):

        return {
            "type": "kpi_cards",
            "values": numeric_columns,
            "reason": (
                "The result contains multiple numeric KPIs "
                "in a single row, so KPI cards are appropriate."
            )
        }

    # ========================================================
    # 5. GEOGRAPHIC DATA
    # ========================================================

    if (
        len(geo_columns) >= 1
        and len(numeric_columns) >= 1
    ):

        geo_column = geo_columns[0]
        numeric_column = numeric_columns[0]

        # Latitude + longitude
        latitude_columns = [
            column
            for column in df.columns
            if str(column).lower() in [
                "latitude",
                "lat"
            ]
        ]

        longitude_columns = [
            column
            for column in df.columns
            if str(column).lower() in [
                "longitude",
                "lon",
                "lng"
            ]
        ]

        if (
            latitude_columns
            and longitude_columns
        ):

            return {
                "type": "map",
                "location": geo_column,
                "latitude": latitude_columns[0],
                "longitude": longitude_columns[0],
                "size": numeric_column,
                "reason": (
                    "The result contains geographic coordinates "
                    "and a numeric measure, so a map is appropriate."
                )
            }

        return {
            "type": "map",
            "location": geo_column,
            "value": numeric_column,
            "reason": (
                "The result contains geographic data and a numeric "
                "measure, so a geographic visualization is appropriate."
            )
        }

    # ========================================================
    # 6. TIME + NUMERIC
    # ========================================================

    if (
        len(time_columns) >= 1
        and len(numeric_columns) >= 1
    ):

        time_column = time_columns[0]

        # Multiple numeric columns over time
        if len(numeric_columns) >= 2:

            return {
                "type": "multi_line",
                "x": time_column,
                "y": numeric_columns,
                "reason": (
                    "The result contains time-based data with multiple "
                    "numeric measures, so a multi-line chart is suitable "
                    "for comparing trends."
                )
            }

        numeric_column = numeric_columns[0]

        return {
            "type": "line",
            "x": time_column,
            "y": numeric_column,
            "reason": (
                "The result contains time-based and numeric values, "
                "so a line chart is suitable for showing trends."
            )
        }

    # ========================================================
    # 7. TWO CATEGORICAL DIMENSIONS
    # ========================================================

    if (
        len(categorical_columns) >= 2
        and len(numeric_columns) >= 1
    ):

        return {
            "type": "heatmap",
            "x": categorical_columns[0],
            "y": categorical_columns[1],
            "value": numeric_columns[0],
            "reason": (
                "The result contains two categorical dimensions "
                "and a numeric measure, so a heatmap is useful "
                "for comparing combinations."
            )
        }

    # ========================================================
    # 8. CATEGORY + NUMERIC
    # ========================================================

    if (
        len(categorical_columns) >= 1
        and len(numeric_columns) >= 1
    ):

        category_column = categorical_columns[0]
        numeric_column = numeric_columns[0]

        # Percentage/proportion data
        if _looks_like_percentage(
            df[numeric_column]
        ) and len(df) <= 10:

            return {
                "type": "donut",
                "labels": category_column,
                "values": numeric_column,
                "reason": (
                    "The result contains a small number of categories "
                    "with proportional numeric values, so a donut chart "
                    "is appropriate."
                )
            }

        # Ranking data
        category_name = str(
            category_column
        ).lower()

        if any(
            keyword in category_name
            for keyword in [
                "rank",
                "product",
                "customer",
                "item",
                "name"
            ]
        ) and len(df) <= 15:

            return {
                "type": "horizontal_bar",
                "x": numeric_column,
                "y": category_column,
                "reason": (
                    "The result resembles a ranking, so a horizontal "
                    "bar chart makes comparison easier."
                )
            }

        return {
            "type": "bar",
            "x": category_column,
            "y": numeric_column,
            "reason": (
                "The result contains categorical and numeric values, "
                "so a bar chart is suitable for comparison."
            )
        }

    # ========================================================
    # 9. TWO OR MORE NUMERIC COLUMNS
    # ========================================================

    if len(numeric_columns) >= 2:

        return {
            "type": "scatter",
            "x": numeric_columns[0],
            "y": numeric_columns[1],
            "reason": (
                "The result contains multiple numeric variables, "
                "so a scatter plot is suitable for showing relationships."
            )
        }

    # ========================================================
    # 10. SINGLE NUMERIC COLUMN
    # ========================================================

    if len(numeric_columns) == 1:

        return {
            "type": "histogram",
            "x": numeric_columns[0],
            "reason": (
                "The result contains one numeric variable across "
                "multiple rows, so a histogram can show its distribution."
            )
        }

    # ========================================================
    # 11. FALLBACK
    # ========================================================

    return {
        "type": "table",
        "reason": (
            "The result structure does not clearly match a chart type, "
            "so displaying the data as a table is most appropriate."
        )
    }