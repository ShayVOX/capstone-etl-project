import pandas as pd
from .logger import get_logger

logger = get_logger("kpis")


# Fuel group definitions


LOW_CARBON_FUELS = [
    "nuclear",
    "hydro",
    "wind",
    "solar",
    "other_renewables",
    "geothermal",
    "combustible_renewables",
]

FOSSIL_FUELS = [
    "coal",
    "natural_gas",
    "oil",
    "other_combustible_non-renewables",
]


# Production KPIs


def calculate_generation_mix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds energy generation KPIs to the electricity production fact table:
      - total_generation_gwh
      - low_carbon_gwh
      - fossil_gwh
      - low_carbon_share_pct
      - fossil_share_pct

    Works directly from fuel columns present in your production fact data.
    """

    logger.info("Calculating generation mix KPIs")

    df = df.copy()

    # ---- Total generation ----
    # Sum all fuels + not_specified to derive true monthly total
    df["total_generation_gwh"] = (
        df[LOW_CARBON_FUELS + FOSSIL_FUELS + ["not_specified"]]
        .sum(axis=1)
    )

    # ---- Category totals ----
    df["low_carbon_gwh"] = df[LOW_CARBON_FUELS].sum(axis=1)
    df["fossil_gwh"] = df[FOSSIL_FUELS].sum(axis=1)

    # ---- Percentage shares ----
    df["low_carbon_share_pct"] = (
        df["low_carbon_gwh"] / df["total_generation_gwh"] * 100
    )

    df["fossil_share_pct"] = (
        df["fossil_gwh"] / df["total_generation_gwh"] * 100
    )

    logger.info("Generation KPI calculations complete")

    return df


# Trade KPIs


def calculate_trade_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds trade/security KPIs to the electricity trade fact table:
      - net_imports_gwh
      - import_dependency_pct

    Expects these base columns:
      - total_imports
      - total_exports
      - net_electricity_production
    """

    logger.info("Calculating trade KPIs")

    df = df.copy()

    # ---- Net imports ----
    df["net_imports_gwh"] = df["total_imports"] - df["total_exports"]

    # ---- Import dependency ----
    # % of usage met via net imports
    df["import_dependency_pct"] = (
        df["net_imports_gwh"]
        / (df["net_imports_gwh"] + df["net_electricity_production"])
        * 100
    )

    logger.info("Trade KPI calculations complete")

    return df
