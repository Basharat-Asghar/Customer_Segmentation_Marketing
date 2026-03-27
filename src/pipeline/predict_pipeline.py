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
            
            # Debug: Log model info
            logger.info(f"Model type: {type(model)}")
            if hasattr(model, 'n_clusters'):
                logger.info(f"Model n_clusters: {model.n_clusters}")
            if hasattr(model, 'cluster_centers_'):
                logger.info(f"Model cluster centers shape: {model.cluster_centers_.shape}")
                logger.info(f"Model cluster centers:\n{model.cluster_centers_}")
            
            logger.info("Artifacts loaded successfully...")
            return preprocessor, model

        except Exception as e:
            raise CustomException("Can't load artifacts", sys)
    
    def _convert_to_int(self, value):
        """Safely convert a value to integer for mapping"""
        if pd.isna(value):
            return value
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return value
        
    def predict(self, input_data):
        try:
            logger.info("Starting prediction pipeline...")

            logger.info("Loading Artifacts...")
            preprocessor, model = self._load_artifacts()

            df = input_data.copy()
            
            # Debug: Log input data
            logger.info(f"Input data shape: {df.shape}")
            logger.info(f"Input data columns: {df.columns.tolist()}")
            logger.info(f"Input data:\n{df}")

            logger.info("Performing log1p transformation on clustering features...")
            log_transform_cols = self.config.log_transform_columns
            for col in log_transform_cols:
                log_col = f"log_{col.split('_')[0] if '_' in col else col.lower()}"
                df[log_col] = np.log1p(df[col])
                logger.info(f"Created {log_col}: min={df[log_col].min():.4f}, max={df[log_col].max():.4f}")

            # Debug: Check features before preprocessing
            features_before = df[self.config.clustering_features]
            logger.info(f"Features before preprocessing:\n{features_before}")
            logger.info(f"Features stats:\n{features_before.describe()}")

            df_process = preprocessor.transform(df[self.config.clustering_features])
            
            # Debug: Check features after preprocessing
            logger.info(f"Features after preprocessing shape: {df_process.shape}")
            logger.info(f"Features after preprocessing:\n{df_process}")
            if hasattr(df_process, 'mean'):
                logger.info(f"Processed features mean: {df_process.mean(axis=0)}")
                logger.info(f"Processed features std: {df_process.std(axis=0)}")

            logger.info("Performing preprocessing on features...")
            X = df_process

            logger.info("Predicting clusters for customers...")
            
            # Debug: If model has predict_proba or decision_function
            if hasattr(model, 'transform'):
                distances = model.transform(X)
                logger.info(f"Distances to cluster centers:\n{distances}")
            
            labels = model.predict(X)
            logger.info(f"Raw predictions: {labels}")
            logger.info(f"Unique predictions: {np.unique(labels)}")
            logger.info(f"Prediction counts: {pd.Series(labels).value_counts().to_dict()}")

            df['cluster'] = labels

            # Convert mapping keys to integers
            personas_map = {int(k): v for k, v in self.config.personas.items()}
            region_map = {int(k): v for k, v in self.config.region.items()}
            channel_map = {int(k): v for k, v in self.config.channel.items()}

            # Map cluster to persona with fallback
            df['persona'] = df["cluster"].map(personas_map)
            if df['persona'].isna().any():
                missing_clusters = df[df['persona'].isna()]['cluster'].unique()
                logger.warning(f"Missing persona mappings for clusters: {missing_clusters}")
                df['persona'] = df['persona'].fillna(df['cluster'].apply(lambda x: f"Cluster_{x}"))

            # Convert region and channel to integers before mapping
            df["region"] = df["region"].apply(self._convert_to_int)
            df["channel"] = df["channel"].apply(self._convert_to_int)

            # Map region and channel
            df["region"] = df["region"].map(region_map).fillna("Unknown")
            df['channel'] = df['channel'].map(channel_map).fillna("Unknown")

            # Save predictions
            write_json(
                self.config.predicted_data,
                df.to_dict(orient='records')
            )
            logger.info(f"Predictions saved at: {self.config.predicted_data}")

            return df

        except Exception as e:
            raise CustomException("Error in prediction", sys)