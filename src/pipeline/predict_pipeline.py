import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import PredictPipelineConfig
from src.utils.common import load_object, write_json

logger = get_logger(__name__)

class PredictPipeline:
    def __init__(self, config: PredictPipelineConfig):
        self.config = config

    def _load_artifacts(self):
        try:
            logger.info("Loading artifacts...")
            preprocessor = load_object(self.config.preprocessor_path)
            model = load_object(self.config.final_model_path)
            logger.info("Artifacts loaded successfully...")

            return (
                preprocessor,
                model
            )

        except Exception as e:
            raise CustomException("Can't load artifacts", sys)
        
    def predict(self, input_data):
        try:
            logger.info("Starting prediction pipeline...")

            logger.info("Loading Artifacts...")
            preprocessor, model = self._load_artifacts()

            df = input_data.copy()

            logger.info("Performing log1p transformation on clustering features...")
            log_transform_cols = self.config.log_transform_columns
            for col in log_transform_cols:
                log_col = f"log_{col.split('_')[0] if '_' in col else col.lower()}"
                df[log_col] = np.log1p(df[col])

            df_process = preprocessor.transform(df[self.config.clustering_features])
                
            logger.info("Performing preprocessing on features...")
            X = df_process

            logger.info("Predicting clusters for customers...")
            labels = model.predict(X)

            df['cluster'] = labels

            personas_map = self.config.personas
            region_map = self.config.region
            channel_map = self.config.channel

            df['persona'] = df["cluster"].map(personas_map)
            df["region"] = df["region"].map(region_map)
            df['channel'] = df['channel'].map(channel_map)

            write_json(
                self.config.predicted_data,
                df.to_dict(orient='records')
            )
            logger.info(f"Predictions saved at: {self.config.predicted_data}")

            return df

        except Exception as e:
            raise CustomException("Error in prediction", sys)

