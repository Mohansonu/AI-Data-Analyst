import io

import pandas as pd


# ============================================================
# DATAFRAME → CSV
# ============================================================

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert a DataFrame into CSV bytes
    suitable for Streamlit download.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None")

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ============================================================
# DATAFRAME → EXCEL
# ============================================================

def dataframe_to_excel(df: pd.DataFrame) -> bytes:
    """
    Convert a DataFrame into an Excel file.

    Returns:
        bytes: Excel file content.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None")

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Query Result"
        )

    output.seek(0)

    return output.getvalue()