# scripts/build_dim_country.py

import pandas as pd
from pathlib import Path

prod = pd.read_csv("data/output/fact_electricity_production_monthly.csv")
trade = pd.read_csv("data/output/fact_electricity_trade_monthly.csv")

countries = pd.concat([
    prod["country"],
    trade["country"]
]).dropna().drop_duplicates().sort_values()

dim_country = pd.DataFrame({
    "country_id": range(1, len(countries) + 1),
    "country": countries.values
})

output_path = Path("data/output/dim_country.csv")
dim_country.to_csv(output_path, index=False)

print("dim_country built")
print(dim_country.head())
print("Total countries:", len(dim_country))
