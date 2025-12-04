import pandas as pd
from pathlib import Path


# PATHS

RAW_PATH = Path("data/raw/monthly_electricity_data_0825.csv")
OUT_PATH = Path("data/processed/oecd_energy_fact.csv")


# FILTERS

OECD_COUNTRIES = [
    "Australia","Austria","Belgium","Canada","Czech Republic","Denmark",
    "Estonia","Finland","France","Germany","Greece","Hungary","Iceland",
    "Ireland","Italy","Japan","Korea","Latvia","Lithuania","Luxembourg",
    "Mexico","Netherlands","New Zealand","Norway","Poland","Portugal",
    "Slovak Republic","Slovenia","Spain","Sweden","Switzerland",
    "Republic of Turkiye","United Kingdom","United States"
]

VALID_BALANCES = [
    "Net Electricity Production",
    "Total Imports",
    "Total Exports",
    "Final Consumption (Calculated)",
    "Distribution Losses"
]


# PRODUCT CLEANUP

PRODUCT_RENAMES = {
    "Coal, Peat and Manufactured Gases": "Coal",
    "Oil and Petroleum Products": "Oil",
}

LOW_CARBON = {
    "Hydro",
    "Wind",
    "Solar",
    "Geothermal",
    "Other Renewables",
    "Combustible Renewables",
}

FOSSIL = {
    "Coal",
    "Oil",
    "Natural Gas",
    "Other Combustible Non-Renewables",
}

VALIDATION_TOTALS = {
    "Electricity",
    "Total Renewables (Hydro, Geo, Solar, Wind, Other)",
    "Total Combustible Fuels",
}


# MAIN PIPELINE

def main():
    print("🔹 Reading raw file...")
    df = pd.read_csv(RAW_PATH, low_memory=False)


    # DATE ENGINEERING

    df["Time_dt"] = pd.to_datetime(df["Time"], format="%b-%y", errors="coerce")
    df["year"] = df["Time_dt"].dt.year
    df["month"] = df["Time_dt"].dt.month
    df["year_month"] = df["Time_dt"].dt.to_period("M").astype(str)

    df = df[(df["Time_dt"] >= "2015-01-01") & (df["Time_dt"] <= "2025-12-31")]


    # COUNTRY FILTER

    df["is_oecd_member"] = df["Country"].isin(OECD_COUNTRIES)
    df = df[df["is_oecd_member"]]


    # BALANCE FILTER

    df = df[df["Balance"].isin(VALID_BALANCES)]


    # CLEAN PRODUCT NAMES

    df["product_clean"] = df["Product"].replace(PRODUCT_RENAMES)

    # CLASSIFICATION FLAGS

    df["is_atomic_fuel"] = df["product_clean"].isin(
        LOW_CARBON | FOSSIL | {"Nuclear"}
    )

    df["fuel_group"] = "OTHER"
    df.loc[df["product_clean"].isin(LOW_CARBON), "fuel_group"] = "LOW_CARBON"
    df.loc[df["product_clean"].isin(FOSSIL), "fuel_group"] = "FOSSIL"
    df.loc[df["product_clean"] == "Nuclear", "fuel_group"] = "NUCLEAR"

    df["is_validation_total"] = df["Product"].isin(VALIDATION_TOTALS)


    # FINAL OUTPUT

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("OECD PROCESSED DATASET CREATED")
    print(f"   Output file: {OUT_PATH}")
    print(f"   Row count: {len(df):,}")

    print("\nSample rows:")
    print(df[[
        "Country",
        "Time",
        "Balance",
        "Product",
        "product_clean",
        "fuel_group",
        "is_atomic_fuel",
        "is_validation_total",
        "Value",
        "Unit"
    ]].head())


if __name__ == "__main__":
    main()
