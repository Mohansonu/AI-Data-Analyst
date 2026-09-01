import pandas as pd

from app.services.visualization_service import create_visualization


def test_category_revenue_returns_bar():

    df = pd.DataFrame({
        "category": [
            "Sports",
            "Fashion",
            "Home",
            "Books",
            "Electronics"
        ],
        "revenue": [
            1000,
            900,
            800,
            700,
            600
        ]
    })

    result = create_visualization(df)

    assert result["type"] == "bar"


def test_monthly_revenue_returns_line():

    df = pd.DataFrame({
        "month": [
            "2026-01",
            "2026-02",
            "2026-03"
        ],
        "revenue": [
            1000,
            1500,
            2000
        ]
    })

    result = create_visualization(df)

    assert result["type"] == "line"


def test_two_numeric_columns_returns_scatter():

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

    result = create_visualization(df)

    assert result["type"] == "scatter"


def test_empty_dataframe():

    df = pd.DataFrame()

    result = create_visualization(df)

    assert result["type"] == "none"