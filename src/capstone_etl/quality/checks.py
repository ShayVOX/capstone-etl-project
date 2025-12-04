import pandas as pd



# GENERIC CHECKS


def check_not_empty(df: pd.DataFrame, name: str):
    if df.empty:
        raise ValueError(f"[QUALITY FAIL] {name} is empty.")


def check_unique_key(df: pd.DataFrame, columns: list[str], name: str):
    duplicates = df[df.duplicated(columns, keep=False)]
    if not duplicates.empty:
        raise ValueError(
            f"[QUALITY FAIL] {name} has duplicate primary keys on {columns}"
        )


def check_non_negative(df: pd.DataFrame, numeric_cols: list[str], name: str):
    for c in numeric_cols:
        if (df[c].dropna() < 0).any():
            raise ValueError(
                f"[QUALITY FAIL] {name} contains negative values in '{c}'"
            )


def check_null_threshold(
    df: pd.DataFrame,
    max_null_ratio: float,
    exempt_cols: list[str],
    name: str,
):
    for col in df.columns:
        if col in exempt_cols:
            continue

        null_ratio = df[col].isnull().mean()
        if null_ratio > max_null_ratio:
            raise ValueError(
                f"[QUALITY FAIL] {name}.{col} null ratio {null_ratio:.2%} exceeds threshold {max_null_ratio:.2%}"
            )


# FACT TABLE QC


def validate_production_fact(df: pd.DataFrame):
    name = "fact_electricity_production_monthly"

    check_not_empty(df, name)
    check_unique_key(df, ["country", "year", "month"], name)

    numeric_cols = df.select_dtypes("number").columns.tolist()
    check_non_negative(df, numeric_cols, name)

    check_null_threshold(
        df,
        max_null_ratio=0.50,       # fuels can be sparse by geography
        exempt_cols=["not_specified"],
        name=name
    )


def validate_trade_fact(df: pd.DataFrame):
    name = "fact_electricity_trade_monthly"

    check_not_empty(df, name)
    check_unique_key(df, ["country", "year", "month"], name)

    numeric_cols = df.select_dtypes("number").columns.tolist()
    check_non_negative(df, numeric_cols, name)

    check_null_threshold(
        df,
        max_null_ratio=0.40,
        exempt_cols=[],
        name=name
    )
