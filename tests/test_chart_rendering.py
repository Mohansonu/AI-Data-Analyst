import pandas as pd

from app.services.visualization_service import create_visualization
from app.services.chart_service import render_chart


def test_render_bar_chart():

    df = pd.DataFrame({
        "category": [
            "Sports",
            "Fashion",
            "Home"
        ],
        "revenue": [
            1000,
            900,
            800
        ]
    })

    visualization = create_visualization(df)

    chart = render_chart(
        df,
        visualization
    )

    assert chart is not None
    assert chart.data[0].type == "bar"


def test_render_line_chart():

    df = pd.DataFrame({
        "month": [
            "January",
            "February",
            "March"
        ],
        "revenue": [
            1000,
            1200,
            1500
        ]
    })

    visualization = create_visualization(df)

    chart = render_chart(
        df,
        visualization
    )

    assert chart is not None
    assert chart.data[0].type == "scatter"


def test_render_scatter_chart():

    df = pd.DataFrame({
        "quantity": [
            10,
            20,
            30
        ],
        "revenue": [
            100,
            250,
            400
        ]
    })

    visualization = create_visualization(df)

    chart = render_chart(
        df,
        visualization
    )

    assert chart is not None
    assert chart.data[0].type == "scatter"


def test_render_empty_dataframe():

    df = pd.DataFrame()

    visualization = create_visualization(df)

    chart = render_chart(
        df,
        visualization
    )

    assert chart is None