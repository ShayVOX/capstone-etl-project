import pandas as pd
from pathlib import Path

from transform.transform import (
    standardise_dataset_1,
    standardise_dataset_2,
    pivot_balance_features,
    clean_pivot_dataset,
    pivot_production_fuels
)


# DATASET 1


def extract_dataset_1() -> pd.DataFrame:
    path = Path("data/raw/iea_electricity_production.csv")

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    return pd.read_csv(path)



# DATASET 2


def extract_dataset_2() -> pd.DataFrame:
    path = Path("data/raw/monthly_electricity_data_0825.csv")

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    return pd.read_csv(path, skiprows=8)


# MAIN (development run)


if __name__ == "__main__":

    print("\n--- DATASET 1 — STANDARDISED ---")
    df1_raw = extract_dataset_1()
    df1 = standardise_dataset_1(df1_raw)
    print(df1.info())
    print(df1.head())

    print("\n--- DATASET 2 — STANDARDISED ---")
    df2_raw = extract_dataset_2()
    df2 = standardise_dataset_2(df2_raw)
    print(df2.info())
    print(df2.head())
    
    # Pivot dataset 2
    print("\n--- DATASET 2 — PIVOTED (RAW) ---")

    pivot_df = pivot_balance_features(df2)

    print(pivot_df.info())
    print(pivot_df.head())

    print("\nRows before cleaning:", len(pivot_df))

    print("\n--- DATASET 2 — PIVOTED & CLEANED ---")

    clean_fact_df = clean_pivot_dataset(pivot_df)

    print(clean_fact_df.info())
    print(clean_fact_df.head())

    print("\nRows after cleaning:", len(clean_fact_df))

    print("\nDistinct countries after cleaning:")
    print(sorted(clean_fact_df["country"].unique())[:20], "...")

    print("\nTotal distinct countries:", clean_fact_df["country"].nunique())
    
 
    # DATASET 1 — PIVOTED FUELS


    print("\n--- DATASET 1 — PIVOTED PRODUCTION FUELS ---")

    fuel_fact = pivot_production_fuels(df1)

    print(fuel_fact.info())
    print(fuel_fact.head())

    output_path = Path("data/output/fact_electricity_production_monthly.csv")

    fuel_fact.to_csv(output_path, index=False)

    print("\n Clean production fact table exported to:")
    print(" -", output_path.resolve())

    

# STEP EXPORT CLEAN FACT TABLE


output_path = Path("data/output/fact_electricity_trade_monthly.csv")

clean_fact_df.to_csv(
    output_path,
    index=False
)

print("\n✅ Clean trade fact table exported to:")
print(f" - {output_path.resolve()}")




# HUMAN VISUAL INSPECTION SNAPSHOTS


print("\n--- EXPORTING SAMPLE VIEWS FOR MANUAL INSPECTION ---")

df1.sample(5000, random_state=42).to_csv(
    "data/output/sample_dataset1_standardised.csv",
    index=False
)

df2.sample(5000, random_state=42).to_csv(
    "data/output/sample_dataset2_standardised.csv",
    index=False
)

print("Samples written to:")
print(" - data/output/sample_dataset1_standardised.csv")
print(" - data/output/sample_dataset2_standardised.csv")


# STEP DATASET 1 PROFILING (NO TRANSFORMS)


print("\n--- DATASET 1 — PRODUCT PROFILING ---")

product_counts = (
    df1
    .groupby("product")
    .size()
    .sort_values(ascending=False)
)

print("\nTotal distinct products:", product_counts.size)

print("\nTop 20 most frequent products:")
print(product_counts.head(20))

print("\nFull product list:")
print(sorted(product_counts.index))
