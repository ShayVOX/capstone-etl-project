import pandas as pd
from pathlib import Path

from capstone_etl.quality.checks import (
    validate_production_fact,
    validate_trade_fact,
)


BASE = Path("data/output")

files = {
    "production": BASE / "fact_electricity_production_monthly.csv",
    "trade": BASE / "fact_electricity_trade_monthly.csv"
}


print("---- RUNNING DATA QUALITY CHECKS ----")

# ------------------------------
# LOAD
# ------------------------------

prod_df = pd.read_csv(files["production"])
trade_df = pd.read_csv(files["trade"])


# ------------------------------
# VALIDATE
# ------------------------------

validate_production_fact(prod_df)
validate_trade_fact(trade_df)


# ------------------------------
# SUCCESS
# ------------------------------

print("✅ All data quality checks PASSED.")
print()
print("Production fact rows:", len(prod_df))
print("Trade fact rows:", len(trade_df))
print("Distinct production countries:", prod_df["country"].nunique())
print("Distinct trade countries:", trade_df["country"].nunique())
