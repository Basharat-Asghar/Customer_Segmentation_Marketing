import pandas as pd
from pathlib import Path
import joblib
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import PersonaAssignmentConfig
from src.utils.common import load_object

logger = get_logger(__name__)

class PersonaBuilder:
    def __init__(self, config: PersonaAssignmentConfig):
        self.config = config

    def _load_data(self, data_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(data_path)

            return df

        except Exception as e:
            raise CustomException("Error in loading data for model training", sys)
        
    def assign_personas(self, data_path: str, model_path: Path):
        try:
            logger.info("Starting the persona assignment process...")
            df = self._load_data(data_path)
            X = df[self.config.clustering_features].values

            logger.info("Loading saved best model, to assign cluster personas...")
            model = load_object(model_path)
            labels = model.predict(X)
            df['cluster'] = labels

            logger.info("Assigning cluster personas...")
            personas_map = self.config.personas
            region_map = self.config.region
            channel_map = self.config.channel
            engagement_tier_map = self.config.engagement_tier
            clv_tier_map = self.config.clv_tier

            df['persona'] = df["cluster"].map(personas_map)
            df["region"] = df["region"].map(region_map)
            df['channel'] = df['channel'].map(channel_map)
            df['engagement_tier'] = df['engagement_tier'].map(engagement_tier_map)
            df['clv_tier'] = df['clv_tier'].map(clv_tier_map)

            df.to_csv(
                self.config.clustered_data_path, index=False
            )
            logger.info(f"Clustered data saved at: {self.config.clustered_data_path}")

            return self.config.clustered_data_path

        except Exception as e:
            raise CustomException("Failed to assign persona to clusters...", sys)