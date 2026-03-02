import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import DataIngestionConfig

logger = get_logger(__name__)

class DataIngestion:
    """
    Fetches data from MySQL and saves to CSV.
    """

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def _create_db_engine(self):
        """
        Creates SQLAlchemy engine.
        """
        try:
            connection_string = (
                f"mysql+pymysql://"
                f"{self.config.db_user}:"
                f"{self.config.db_password}@"
                f"{self.config.db_host}:"
                f"{self.config.db_port}/"
                f"{self.config.db_name}"
            )

            engine = create_engine(connection_string)
            logger.info("DB engine created successfully.")

            return engine
        
        except Exception as e:
            raise CustomException("Failed to create DB engine", sys)

    def export_data_to_csv(self):
        """
        Fetch data from MySQL and save as CSV.
        """

        try:
            logger.info("Starting Data Ingestion from MySQL to CSV...")
            engine = self._create_db_engine()
            query = f"SELECT * FROM {self.config.db_table}"

            df = pd.read_sql(query, con=engine)
            logger.info(f"Fetched {len(df)} record from MySQL Successfully.")

            df.to_csv(self.config.raw_data_path, index=False)
            logger.info(f"Data saved to {self.config.raw_data_path} successfully.")

            return self.config.raw_data_path
        
        except Exception as e:
            raise CustomException("Failed in Data Ingestion", sys)