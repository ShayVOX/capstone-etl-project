import pandas as pd



# COMMON HELPERS


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all column names to snake_case:
    - strip whitespace
    - lowercase
    - replace spaces and hyphens with underscores
    """
    df = df.copy()

    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(" ", "_")
          .str.replace("-", "_")
    )

    return df



# DATASET 1 — PRODUCTION


def standardise_dataset_1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standardisation rules to Dataset 1.
    """
    df = clean_column_names(df)

    # enforce types explicitly
    df["year"] = df["year"].astype("int64")
    df["month"] = df["month"].astype("int64")
    df["value"] = df["value"].astype("float64")

    return df



# DATASET 2 — TRADE / BALANCE


def standardise_dataset_2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standardisation rules to Dataset 2:
    - clean column names
    - strip whitespace from categorical values
    - convert Time -> datetime
    - derive year & month keys
    """
    df = clean_column_names(df)

    # Strip whitespace in key categorical fields
    for col in ["country", "balance", "product"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["time"] = pd.to_datetime(df["time"], format="%b-%y")

    df["year"] = df["time"].dt.year.astype("int64")
    df["month"] = df["time"].dt.month.astype("int64")
    df["value"] = df["value"].astype("float64")

    # drop unit – always GWh, not analytically useful
    if "unit" in df.columns:
        df.drop(columns=["unit"], inplace=True)

    return df



# DATASET 2 — FEATURE RESHAPING (PIVOT BALANCES)


def pivot_balance_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot Dataset 2 so that each BALANCE category becomes a column.

    Index:
      country, year, month

    Columns (examples):
      Net Electricity Production
      Total Imports
      Total Exports
      Used for pumped storage
      Distribution Losses
      Final Consumption (Calculated)

    Values:
      Sum of 'value' (GWh)
    """

    pivot_df = (
        df
        .pivot_table(
            index=["country", "year", "month"],
            columns="balance",
            values="value",
            aggfunc="sum"
        )
        .reset_index()
    )

    # Standardise column names after pivot (snake_case, remove brackets)
    pivot_df.columns = [
        str(c).strip().lower()
              .replace(" ", "_")
              .replace("(", "")
              .replace(")", "")
        for c in pivot_df.columns
    ]

    return pivot_df


# STEP — CLEAN PIVOTED BALANCE FACT TABLE


AGGREGATE_COUNTRIES = {
    "IEA Total",
    "OECD Total",
    "OECD Americas",
    "OECD Europe",
    "OECD Asia Oceania"
}

COUNTRY_STANDARDISATION = {
    "United States of America": "United States",
    "Republic of Turkiye": "Turkiye",
    "People's Republic of China": "China",
}

def clean_pivot_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply business cleaning to pivoted dataset:
    - Remove non-country aggregates
    - Drop remarks balance bucket
    - Standardize country naming
    - Reset index
    """

    df = df.copy()

    # Drop remarks column
    if "remarks" in df.columns:
        df = df.drop(columns=["remarks"])

    # Remove aggregate regions
    df = df[~df["country"].isin(AGGREGATE_COUNTRIES)]

    # Standardize country names
    df["country"] = df["country"].replace(COUNTRY_STANDARDISATION)

    # Clean indexing after filtering
    df = df.reset_index(drop=True)

    return df



# STEP PRODUCTION FUEL FILTER + PIVOT


VALID_FUELS = {
    "Coal",
    "Oil",
    "Natural gas",
    "Nuclear",
    "Hydro",
    "Wind",
    "Solar",
    "Geothermal",
    "Combustible renewables",
    "Other renewables",
    "Other combustible non-renewables",
    "Not specified",
}

def pivot_production_fuels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters production dataset to true fuel categories and pivots wide by fuel type.
    """

    df = df.copy()

    # Clean whitespace on product
    df["product"] = df["product"].astype(str).str.strip()

    # Keep only true fuel categories
    df = df[df["product"].isin(VALID_FUELS)]

    # Pivot into wide fuel matrix
    pivot_df = pd.pivot_table(
        df,
        index=["country", "year", "month"],
        columns="product",
        values="value",
        aggfunc="sum"
    ).reset_index()

    # Clean resulting column names
    pivot_df.columns = [
        col.lower().replace(" ", "_") if isinstance(col, str) else col
        for col in pivot_df.columns
    ]

    return pivot_df
