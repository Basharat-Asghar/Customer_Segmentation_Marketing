from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig,
                                        DataCleaningConfig,
                                        FeatureEngineeringConfig,
                                        DataTransformationConfig)
from src.utils.exception import CustomException

import sys

class ConfigurationManager:
    def __init__(
            self,
            config_file_path = CONFIG_FILE_PATH,
            params_file_path = PARAMS_FILE_PATH,
            schema_file_path = SCHEMA_FILE_PATH):
        
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config.data_ingestion

            create_directories([self.config.data_ingestion.root_dir])

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
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            config = self.config.data_validation
            schema = self.schema.COLUMNS
            create_directories([self.config.data_validation.root_dir])

            data_validation_config = DataValidationConfig(
                root_dir=config.root_dir,
                valid_data_path=config.valid_data_path,
                report_file_path=config.report_file_path,
                all_schema = schema
            )

            return data_validation_config

        except Exception as e:
            raise CustomException("Error in getting Data Validation Config", sys)
        
    def get_data_cleaning_config(self) -> DataCleaningConfig:
        try:
            config = self.config.data_cleaning

            create_directories([self.config.data_cleaning.root_dir])

            data_cleaning_config = DataCleaningConfig(
                root_dir=config.root_dir,
                cleaned_data_path=config.cleaned_data_path,
                duplicate_strategy=config.duplicate_strategy,
                missing_value_strategy=config.missing_value_strategy,
                missing_columns=config.missing_columns 
            )

            return data_cleaning_config
        
        except Exception as e:
            raise CustomException("Error in getting Data Cleaning Config", sys)
        
    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:
        try:
            config = self.config.feature_engineering

            create_directories([self.config.feature_engineering.root_dir])

            feature_engineering_config = FeatureEngineeringConfig(
                root_dir=config.root_dir,
                featured_data_path=config.featured_data_path,
                log_transform_columns=config.log_transform_columns,
                engagement_bins=config.engagement_bins,
                engagement_labels=config.engagement_labels,
                clv_bins=config.clv_bins,
                clv_labels=config.clv_labels
            )

            return feature_engineering_config

        except Exception as e:
            raise CustomException("Error in getting Feature Engineering Config", sys)
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            config = self.config.data_transformation

            create_directories([config.root_dir])

            data_transformation_config = DataTransformationConfig(
                root_dir=config.root_dir,
                transformed_data_path=config.transformed_data_path,
                scaler=config.scaler,
                preprocessor_path=config.preprocessor_path,
                clustering_features=config.clustering_features
            )

            return data_transformation_config

        except Exception as e:
            raise CustomException("Error in getting Data Transformation Config", sys)
