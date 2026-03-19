from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.config.configuration import ConfigurationManager

from src.components.data.data_loader import DataIngestion
from src.components.data.data_validator import DataValidation
from src.components.data.data_cleaner import DataCleaner
from src.components.features.feature_engineering import FeatureEngineering
from src.components.data.data_transformation import DataTransformation
from src.components.models.model_trainer import ModelTrainer

import sys

logger = get_logger(__name__)

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        logger.info("Starting Training Pipeline...")

        try:
            # Step 1: Data Ingestion
            logger.info(f">>>>>> Step 1: Data Ingestion Started... <<<<<<")
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            raw_data_path = data_ingestion.export_data_to_csv()
            logger.info(f">>>>>> Data Ingestion completed. Raw data saved at: {raw_data_path} <<<<<<\nx==========x")

            # Step 2: Data Validation
            logger.info(f">>>>>> Step 2: Data Validation Started... <<<<<<")
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            validated_data_path = data_validation.initiate_data_validation(raw_data_path=raw_data_path)
            logger.info(f">>>>>> Data Validation completed. Validated data saved at: {validated_data_path} <<<<<<\nx==========x")

            # Step 3: Data Cleaning
            logger.info(f">>>>>> Step 3: Data Cleaning Started... <<<<<<")
            data_cleaning_config = config.get_data_cleaning_config()
            data_cleaner = DataCleaner(config=data_cleaning_config)
            cleaned_data_path = data_cleaner.clean(validated_data_path)
            logger.info(f">>>>>> Data Cleaning completed. Cleaned data saved at: {cleaned_data_path} <<<<<<\nx==========x")

            # Step 4: Feature Engineering
            logger.info(f">>>>>> Step 4: Feature Engineering Started... <<<<<<")
            feature_engineering_config = config.get_feature_engineering_config()
            feature_engineer = FeatureEngineering(config=feature_engineering_config)
            featured_data_path = feature_engineer.engineer_features(cleaned_data_path)
            logger.info(f">>>>>> Feature Engineering completed. Featured data saved at: {featured_data_path} <<<<<<\nx==========x")

            # Step 5: Data Transformation
            logger.info(f">>>>>> Step 5: Data Transformation Started... <<<<<<")
            data_transformation_config = config.get_data_transformation_config()
            data_transformer = DataTransformation(config=data_transformation_config)
            transformed_data_path, preprocessor_path = (
                data_transformer.initiate_data_transformation(featured_data_path)
            )
            logger.info(f">>>>>> Data Transformation completed. Transformed data saved at: {transformed_data_path} <<<<<<\n")
            logger.info(f"Preprocessor object saved at: {preprocessor_path} <<<<<<\nx==========x")

            # Step 6: Model Training
            logger.info(f">>>>>> Step 6: Model Training Started... <<<<<<")
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            metrics = model_trainer.train_all_models(transformed_data_path)
            logger.info(f">>>>>> Model Training completed. Metrics saved at: {model_trainer_config.metrics_path} <<<<<<\nx==========x")

            # Step 7: Model Evaluation and Selection
            

        except Exception as e:
            raise CustomException("Error in Training Pipeline", sys)