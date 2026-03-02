from src.constants import CONFIG_FILE_PATH
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig
from src.utils.exception import CustomException

import sys

class ConfigurationManager:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        self.config = read_yaml(config_file_path)
        create_directories([self.config.data_ingestion.root_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config.data_ingestion

            data_ingestion_config = DataIngestionConfig(
                root_dir=config.root_dir,
                db_host=config.db_host,
                db_port=config.db_port,
                db_user=config.db_user,
                db_password=config.db_password,
                db_name=config.db_name,
                db_table=config.db_table,
                raw_data_path=config.raw_data_path
            )

            return data_ingestion_config
        except Exception as e:
            raise CustomException("Error in getting Data Ingestion Config", sys)