import pandas as pd
from pathlib import Path

# Load dimension tables
dim_country = pd.read_csv("data/output/dim_country.csv")
dim_date = pd.read_csv("data/output/dim_date.csv")

# Load fact tables
prod = pd.read_csv("data/output/fact_electricity_production_monthly.csv")
trade = pd.read_csv("data/output/fact_electricity_trade_monthly.csv")

# =============== LINK DIMENSIONS ===============

# Merge country dimension
prod = prod.merge(dim_country, on="country", how="left")
trade = trade.merge(dim_country, on="country", how="left")

# Merge date dimension using year+month
prod = prod.merge(
    dim_date[["date_id","year","month"]],
    on=["year","month"],
    how="left"
)

trade = trade.merge(
    dim_date[["date_id","year","month"]],
    on=["year","month"],
    how="left"
)

# =============== VALIDATE LINKS ===============
assert prod["country_id"].notna().all(), "Missing country_id in production fact"
assert trade["country_id"].notna().all(), "Missing country_id in trade fact"
assert prod["date_id"].notna().all(), "Missing date_id in production fact"
assert trade["date_id"].notna().all(), "Missing date_id in trade fact"

# =============== CLEAN FACTS ===============

def finalise_fact(df):
    return df.drop(columns=["country","year","month"])

prod_star = finalise_fact(prod)
trade_star = finalise_fact(trade)

# =============== OUTPUT ===============

prod_path = Path("data/output/fact_electricity_production_star.csv")
trade_path = Path("data/output/fact_electricity_trade_star.csv")

prod_star.to_csv(prod_path, index=False)
trade_star.to_csv(trade_path, index=False)

print("STAR FACT TABLES BUILT")
print("Production rows:", len(prod_star))
print("Trade rows:", len(trade_star))
print("\nProduction sample:")
print(prod_star.head())

print("\nTrade sample:")
print(trade_star.head())
