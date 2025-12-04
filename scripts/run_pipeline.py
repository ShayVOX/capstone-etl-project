from src.extract.extract import run_extraction
from src.transform.transform import run_transformation
from src.load.load import run_load
from src.utils.logging_utils import get_logger

logger = get_logger("ETL_PIPELINE")

def run_pipeline():
    logger.info("ETL pipeline started.")

    try:
        logger.info("Starting extraction phase...")
        raw_df = run_extraction()
        logger.info("Extraction complete.")

        logger.info("Starting transformation phase...")
        transformed_df = run_transformation(raw_df)
        logger.info("Transformation complete.")

        logger.info("Starting load phase...")
        run_load(transformed_df)
        logger.info("Load phase complete.")

        logger.info("ETL pipeline finished successfully.")

    except Exception as e:
        logger.error("ETL pipeline failed.", exc_info=True)
        raise e


if __name__ == "__main__":
    run_pipeline()
