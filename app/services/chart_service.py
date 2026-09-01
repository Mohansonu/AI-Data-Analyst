import pandas as pd
import plotly.express as px


# ============================================================
# SUPPORTED CHART TYPES
# ============================================================

SUPPORTED_CHART_TYPES = [
    "bar",
    "line",
    "area",
    "scatter",
    "histogram",
    "pie",
    "donut",
    "horizontal_bar",
    "multi_line",
    "heatmap",
    "map",
    "metric",
    "kpi_cards",
    "table",
]


# ============================================================
# HELPER
# ============================================================

def _get_chart_type(visualization):
    """
    Accept either:

    render_chart(df, "bar")

    OR

    render_chart(
        df,
        {
            "type": "bar",
            "x": "category",
            "y": "revenue"
        }
    )
    """

    if isinstance(visualization, dict):

        return visualization.get("type")

    return visualization


# ============================================================
# MAIN CHART RENDERER
# ============================================================

def render_chart(
    df: pd.DataFrame,
    visualization
):
    """
    Render a Plotly chart based on the visualization
    recommendation.

    Returns:
        Plotly Figure
        or None
    """

    if df is None or df.empty:
        return None

    chart_type = _get_chart_type(
        visualization
    )

    # ========================================================
    # BAR
    # ========================================================

    if chart_type == "bar":

        if isinstance(visualization, dict):

            x_column = visualization.get("x")
            y_column = visualization.get("y")

        else:

            categorical = df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "string"
                ]
            ).columns

            numeric = df.select_dtypes(
                include="number"
            ).columns

            if len(categorical) == 0 or len(numeric) == 0:
                return None

            x_column = categorical[0]
            y_column = numeric[0]

        if (
            x_column not in df.columns
            or y_column not in df.columns
        ):
            return None

        return px.bar(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} by {x_column}",
            text_auto=".2s"
        )

    # ========================================================
    # LINE
    # ========================================================

    if chart_type == "line":

        if isinstance(visualization, dict):

            x_column = visualization.get("x")
            y_column = visualization.get("y")

            if (
                x_column not in df.columns
                or y_column not in df.columns
            ):
                return None

        else:

            numeric = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric) < 1:
                return None

            y_column = numeric[0]
            x_column = None

        if x_column:

            return px.line(
                df,
                x=x_column,
                y=y_column,
                markers=True,
                title=f"{y_column} over {x_column}"
            )

        return px.line(
            df,
            y=y_column,
            markers=True,
            title="Line Chart"
        )

    # ========================================================
    # AREA
    # ========================================================

    if chart_type == "area":

        x_column = visualization.get("x")
        y_column = visualization.get("y")

        if (
            x_column not in df.columns
            or y_column not in df.columns
        ):
            return None

        return px.area(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} Trend"
        )

    # ========================================================
    # SCATTER
    # ========================================================

    if chart_type == "scatter":

        if isinstance(visualization, dict):

            x_column = visualization.get("x")
            y_column = visualization.get("y")

        else:

            numeric = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric) < 2:
                return None

            x_column = numeric[0]
            y_column = numeric[1]

        if (
            x_column not in df.columns
            or y_column not in df.columns
        ):
            return None

        return px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}"
        )

    # ========================================================
    # HISTOGRAM
    # ========================================================

    if chart_type == "histogram":

        x_column = (
            visualization.get("x")
            if isinstance(visualization, dict)
            else None
        )

        if not x_column:

            numeric = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric) < 1:
                return None

            x_column = numeric[0]

        if x_column not in df.columns:
            return None

        return px.histogram(
            df,
            x=x_column,
            title=f"Distribution of {x_column}"
        )

    # ========================================================
    # PIE
    # ========================================================

    if chart_type == "pie":

        labels = visualization.get("labels")
        values = visualization.get("values")

        if (
            labels not in df.columns
            or values not in df.columns
        ):
            return None

        return px.pie(
            df,
            names=labels,
            values=values,
            title=f"{values} by {labels}"
        )

    # ========================================================
    # DONUT
    # ========================================================

    if chart_type == "donut":

        labels = visualization.get("labels")
        values = visualization.get("values")

        if (
            labels not in df.columns
            or values not in df.columns
        ):
            return None

        return px.pie(
            df,
            names=labels,
            values=values,
            hole=0.5,
            title=f"{values} by {labels}"
        )

    # ========================================================
    # HORIZONTAL BAR
    # ========================================================

    if chart_type == "horizontal_bar":

        x_column = visualization.get("x")
        y_column = visualization.get("y")

        if (
            x_column not in df.columns
            or y_column not in df.columns
        ):
            return None

        return px.bar(
            df,
            x=x_column,
            y=y_column,
            orientation="h",
            title=f"{x_column} Ranking",
            text_auto=".2s"
        )

    # ========================================================
    # MULTI-LINE
    # ========================================================

    if chart_type == "multi_line":

        x_column = visualization.get("x")
        y_columns = visualization.get("y", [])

        if x_column not in df.columns:
            return None

        valid_columns = [
            column
            for column in y_columns
            if column in df.columns
        ]

        if not valid_columns:
            return None

        melted = df[
            [x_column] + valid_columns
        ].melt(
            id_vars=x_column,
            var_name="metric",
            value_name="value"
        )

        return px.line(
            melted,
            x=x_column,
            y="value",
            color="metric",
            markers=True,
            title="Multiple Trends"
        )

    # ========================================================
    # HEATMAP
    # ========================================================

    if chart_type == "heatmap":

        x_column = visualization.get("x")
        y_column = visualization.get("y")
        value_column = visualization.get("value")

        if not all(
            column in df.columns
            for column in [
                x_column,
                y_column,
                value_column
            ]
        ):
            return None

        pivot = df.pivot_table(
            index=y_column,
            columns=x_column,
            values=value_column,
            aggfunc="sum",
            fill_value=0
        )

        return px.imshow(
            pivot,
            text_auto=True,
            aspect="auto",
            title=f"{value_column} Heatmap"
        )

    # ========================================================
    # MAP
    # ========================================================

    if chart_type == "map":

        latitude = visualization.get("latitude")
        longitude = visualization.get("longitude")
        size = visualization.get("size")

        # Coordinate-based map
        if (
            latitude in df.columns
            and longitude in df.columns
        ):

            return px.scatter_map(
                df,
                lat=latitude,
                lon=longitude,
                size=size if size in df.columns else None,
                zoom=3,
                title="Geographic Distribution"
            )

        # Geographic name fallback
        location = visualization.get("location")
        value = visualization.get("value")

        if (
            location in df.columns
            and value in df.columns
        ):

            return px.bar(
                df,
                x=location,
                y=value,
                title=(
                    f"Geographic Distribution: "
                    f"{value} by {location}"
                )
            )

        return None

    # ========================================================
    # Unsupported visualizations
    # ========================================================

    return None