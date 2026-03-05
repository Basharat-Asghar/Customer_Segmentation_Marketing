import pandas as pd
import joblib
import sys
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

from src.entity.config_entity import DataTransformationConfig
from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.utils.common import save_object

logger = get_logger(__name__)

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def _get_preprocessor(self):
        try:
            clustering_features = self.config.clustering_features

            scaler_pipeline = Pipeline(
                steps=[
                    ('scaler', StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ('scaler', scaler_pipeline, clustering_features)
                ]
            )
            logger.info("Preprocessor created")

            return preprocessor

        except Exception as e:
            raise CustomException("Error in getting preprocessor object", sys)
        

    def initiate_data_transformation(self, featured_data_path: str):
        try:
            logger.info("Starting Data Transformation...")
            clustering_features = self.config.clustering_features
            df = pd.read_csv(featured_data_path)

            preprocessor = self._get_preprocessor()

            # Fit + transform (no split in clustering)
            transform_arr = preprocessor.fit_transform(df[clustering_features])

            # Save preprocessor
            save_object(
                file_path=self.config.preprocessor_path,
                obj=preprocessor
            )
            logger.info("Preprocessor saved")

            for i, feat in enumerate(clustering_features):
                df[f"{feat}_scaled"] = transform_arr[:, i]

            df.to_csv(
                self.config.transformed_data_path,
                index=False
            )
            logger.info(f"Data Transformation completed. Transformed data saved at: {self.config.transformed_data_path}")

            return (
                self.config.transformed_data_path,
                self.config.preprocessor_path
            )

        except Exception as e:
            raise CustomException("Error in Data Transformation", sys)