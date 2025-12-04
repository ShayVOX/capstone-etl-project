import pandas as pd
from pathlib import Path
from .logger import get_logger

logger = get_logger("data_loader")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "output"


@pd.api.extensions.register_dataframe_accessor("validate")
class Validator:
    def __init__(self, pandas_obj):
        self._df = pandas_obj

    def not_null(self, cols):
        for col in cols:
            if self._df[col].isnull().any():
                raise ValueError(f"Null values found in column: {col}")
        return self._df

    def unique_key(self, cols):
        if self._df.duplicated(subset=cols).any():
            raise ValueError(f"Duplicate primary keys detected on columns: {cols}")
        return self._df


def load_csv(filename: str) -> pd.DataFrame:
    """Generic CSV loader with logging"""
    path = DATA_DIR / filename

    if not path.exists():
        logger.error(f"File not found: {filename}")
        raise FileNotFoundError(filename)

    logger.info(f"Loading {filename}")
    df = pd.read_csv(path)

    logger.info(f"{filename}: {len(df)} rows loaded")

    return df


def load_dimensions():
    logger.info("Loading dimension tables")

    dim_country = load_csv("dim_country.csv").validate.unique_key(["country_id"])
    dim_date = load_csv("dim_date.csv").validate.unique_key(["date_id"])

    return dim_country, dim_date


def load_facts():
    """
    Loads fact tables and ADDS surrogate dimensional keys
    WITHOUT removing natural keys (country, year, month).
    """

    logger.info("Loading dimension tables")
    dim_country, dim_date = load_dimensions()

    logger.info("Loading raw fact tables")
    prod_raw = load_csv("fact_electricity_production_monthly.csv")
    trade_raw = load_csv("fact_electricity_trade_monthly.csv")

    logger.info("Joining production facts to dimensions")

    prod = (
        prod_raw
        .merge(dim_country, on="country", how="left")
        .merge(dim_date, on=["year", "month"], how="left")
    )

    logger.info("Joining trade facts to dimensions")

    trade = (
        trade_raw
        .merge(dim_country, on="country", how="left")
        .merge(dim_date, on=["year", "month"], how="left")
    )

    # Validate new surrogate keys exist
    for df, name in [(prod, "Production"), (trade, "Trade")]:

        if df["country_id"].isnull().any():
            raise ValueError(f"{name} fact has null country_id after dimension join")

        if df["date_id"].isnull().any():
            raise ValueError(f"{name} fact has null date_id after dimension join")

        logger.info(f"{name} fact resolved to dimensional keys")

    # Validate star-grain uniqueness
    prod.validate.unique_key(["country_id", "date_id"])
    trade.validate.unique_key(["country_id", "date_id"])

    logger.info("Star schema facts ready with natural + surrogate keys")

    return prod, trade

