from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.components.data.data_loader import DataIngestion

import sys

logger = get_logger(__name__)

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        logger.info("Starting Training Pipeline...")

        try:
            # Step 1: Data Ingestion
            logger.info(f">>>>>> Step 1: Data Ingestion Started. <<<<<<")
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            raw_data_path = data_ingestion.export_data_to_csv()
            logger.info(f">>>>>> Data Ingestion completed. Raw data saved at: {raw_data_path} <<<<<<\n\nx==========x")

        except Exception as e:
            raise CustomException("Error in Training Pipeline", sys)