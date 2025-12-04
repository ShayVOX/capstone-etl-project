from capstone_etl.analytics.data_loader import load_facts
from capstone_etl.analytics.kpis import (
    calculate_generation_mix,
    calculate_trade_metrics,
)
from capstone_etl.analytics.logger import get_logger


logger = get_logger("smoke_test")


def main():
    logger.info("=== SMOKE TEST STARTED ===")

    # 1. Load fact tables
    prod, trade = load_facts()
    logger.info(f"Production fact shape: {prod.shape}")
    logger.info(f"Trade fact shape: {trade.shape}")

    # 2. Calculate KPIs
    prod_kpis = calculate_generation_mix(prod)
    trade_kpis = calculate_trade_metrics(trade)

    # 3. Print a small sample to console
    print("\n=== Production KPIs sample ===")
    print(
        prod_kpis[
            [
                "country_id",
                "date_id",
                "low_carbon_gwh",
                "low_carbon_share_pct",
                "fossil_gwh",
                "fossil_share_pct",
            ]
        ].head()
    )

    print("\n=== Trade KPIs sample ===")
    print(
        trade_kpis[
            [
                "country_id",
                "date_id",
                "net_imports_gwh",
                "import_dependency_pct",
            ]
        ].head()
    )

    logger.info("=== SMOKE TEST COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
