import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/monthly_electricity_data_0825.csv")

df = pd.read_csv(RAW_PATH, low_memory=False)

print("\n=== ACTUAL COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== UNIQUE BALANCE VALUES ===")
print(sorted(df["Balance"].dropna().unique()))

print("\n=== UNIQUE PRODUCT VALUES ===")
print(sorted(df["Product"].dropna().unique()))

print("\n=== UNIQUE COUNTRIES (first 50) ===")
print(sorted(df["Country"].dropna().unique())[:50])
