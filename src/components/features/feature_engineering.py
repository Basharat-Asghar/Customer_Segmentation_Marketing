import pandas as pd
import numpy as np
import sys
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import FeatureEngineeringConfig

logger = get_logger(__name__)

class FeatureEngineering:
    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config

    def engineer_features(self, cleaned_data_path: str):
        """
        Apply all feature engineering steps to a cleaned DataFrame.

        Steps:
        1. log1p transform on minutes_watched and CLV.
        2. Ordinal engagement tier binning.
        3. Ordinal CLV tier binning.
        4. Engagement-value ratio (descriptor, capped at 99th pct).

        Parameters
        ----------
        cleaned_data_path : str
            Path to the cleaned CSV data file.
        Returns
        -------
        df_features — DataFrame with all engineered columns appended.
        """

        try:
            df = pd.read_csv(cleaned_data_path)
            df_out  = df.copy()
            logger.info(f"Feature engineering started. Input shape: {df_out.shape}")
            
            # ── Step 1: log1p transforms ──────────────────────────────────────────────
            log_transform_cols = self.config.log_transform_columns
            for col in log_transform_cols:
                log_col = f"log_{col.split('_')[0] if '_' in col else col.lower()}"
                df_out[log_col] = np.log1p(df_out[col])
                logger.info(
                    f"log1p('{col}') -> '{log_col}'  "
                    f"skew: {df_out[col].skew():.2f} -> {df_out[log_col].skew():.2f}"
                )

            # ── Step 2: Engagement tier ───────────────────────────────────────────────
            engagement_bins = self.config.engagement_bins
            engagement_labels = self.config.engagement_labels
            df_out['engagement_tier'] = pd.cut(
                df_out['minutes_watched'],
                bins=engagement_bins,
                labels=engagement_labels,
            ).astype(int)
            logger.info(
                f"Engagement tier distribution: "
                f"{df_out['engagement_tier'].value_counts().sort_index().to_dict()}"
            )

            # ── Step 3: CLV tier ─────────────────────────────────────────────────────
            clv_bins = self.config.clv_bins
            clv_labels = self.config.clv_labels
            df_out['clv_tier'] = pd.cut(
                df_out['CLV'],
                bins=clv_bins,
                labels=clv_labels,
            ).astype(int)
            logger.info(
                f"CLV tier distribution: "
                f"{df_out['clv_tier'].value_counts().sort_index().to_dict()}"
            )

            # ── Step 4: Engagement-value ratio ────────────────────────────────────────
            # Epsilon prevents division by zero for CLV = 0 users.
            df_out["engagement_value_ratio"] = (
                df_out["log_minutes"] / (df_out["log_clv"] + 1e-6)
            )
            cap_99 = df_out["engagement_value_ratio"].quantile(0.99)
            df_out["engagement_value_ratio"] = df_out["engagement_value_ratio"].clip(upper=cap_99)
            logger.info(f"Engagement-value ratio: 99th-pct cap applied at {cap_99:.2f}")

            logger.info(f"Feature engineering complete. Output shape: {df_out.shape}")

            df_out.to_csv(
                self.config.featured_data_path,
                index=False
            )
            logger.info(f"Featured data saved at: {self.config.featured_data_path}")

            return self.config.featured_data_path

        except Exception as e:
            raise CustomException("Error in Feature Engineering", sys)
