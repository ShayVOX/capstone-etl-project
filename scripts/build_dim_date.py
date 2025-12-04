import pandas as pd
from pathlib import Path

# Load facts
prod = pd.read_csv("data/output/fact_electricity_production_monthly.csv")
trade = pd.read_csv("data/output/fact_electricity_trade_monthly.csv")

# Collect all distinct year/month combinations
dates = pd.concat([
    prod[["year","month"]],
    trade[["year","month"]]
]).drop_duplicates().sort_values(["year","month"])

# Build calendar fields
dates["date_start"] = pd.to_datetime(
    dates["year"].astype(str) + "-" +
    dates["month"].astype(str).str.zfill(2) + "-01"
)

dates["month_name"] = dates["date_start"].dt.strftime("%B")
dates["year_month"] = dates["date_start"].dt.strftime("%Y-%m")

# Assign surrogate keys
dates = dates.reset_index(drop=True)
dates.insert(0, "date_id", dates.index + 1)

# Save dimension
out_path = Path("data/output/dim_date.csv")
dates.to_csv(out_path, index=False)

print("dim_date built")
print(dates.head())
print("Total dates:", len(dates))
print("Range:", dates["year_month"].min(), "→", dates["year_month"].max())
