import os
from src.fetcher import fetch_latest_stats
from src.scraper import process_local_html
from src.cleaning import clean_raw_data
from src.utils.logger import setup_logger

logger = setup_logger("Main_Pipeline")

def run_pipeline():
    logger.info("🚀 Starting Full EPL Pipeline...")

    if fetch_latest_stats():
        process_local_html()
        clean_raw_data()
        logger.info("🎯 Pipeline Complete!")
    else:
        logger.critical("❌ Pipeline aborted: Fetcher failed.")

if __name__ == "__main__":
    run_pipeline()