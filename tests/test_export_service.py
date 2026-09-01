import pandas as pd

from app.services.export_service import (
    dataframe_to_csv,
    dataframe_to_excel
)


def test_dataframe_to_csv():

    df = pd.DataFrame({
        "product": [
            "Laptop",
            "Phone"
        ],
        "revenue": [
            50000,
            30000
        ]
    })

    result = dataframe_to_csv(df)

    assert isinstance(result, bytes)

    text = result.decode("utf-8")

    assert "product" in text
    assert "revenue" in text
    assert "Laptop" in text
    assert "50000" in text


def test_dataframe_to_csv_without_index():

    df = pd.DataFrame({
        "name": ["A", "B"],
        "value": [10, 20]
    })

    result = dataframe_to_csv(df)

    text = result.decode("utf-8")

    assert "0,A,10" not in text
    assert "name,value" in text


def test_dataframe_to_excel():

    df = pd.DataFrame({
        "product": [
            "Laptop",
            "Phone"
        ],
        "revenue": [
            50000,
            30000
        ]
    })

    result = dataframe_to_excel(df)

    assert isinstance(result, bytes)

    assert len(result) > 0


def test_none_dataframe():

    try:

        dataframe_to_csv(None)

        assert False

    except ValueError:

        assert True