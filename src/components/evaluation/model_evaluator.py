import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import ModelEvaluatorConfig
from src.utils.common import read_json, write_json

logger = get_logger(__name__)

class ModelEvaluator:
    def __init__(self, config: ModelEvaluatorConfig):
        self.config = config

    def _load_metrics(self):
        try:
            logger.info("Loading model metrics...")
            metrics_path = self.config.metrics_path
            metrics = read_json(metrics_path)
            return metrics

        except Exception as e:
            raise CustomException("Error loading model metrics...", sys)
        
    def _normalize(self, series):
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([0.5] * len(series), index=series.index)
        return (series - min_val) / (max_val - min_val)

    def _normalize_metrics(self):
        try:
            logger.info("Starting metrics normalization...")
            weights = self.config.weights
            metrics = self._load_metrics()

            # Validate weights
            required = ['silhouette_score', 'davies_bouldin_score', 'calinski_harabasz_score']
            for w in required:
                if w not in weights:
                    raise ValueError(f"Missing weight: {w}")

            # Flatten metrics into a DataFrame for easier processing
            rows = []

            for model_name, model_metrics in metrics.items():
                for param_key, param_metrics in model_metrics.items():
                    row = {
                    'model': model_name,
                    'clusters': param_key,
                    'silhouette_score': param_metrics.get("silhouette"),
                    'davies_bouldin_score': param_metrics.get("davies_bouldin"),
                    'calinski_harabasz_score': param_metrics.get("calinski_harabasz"),
                    #'n_clusters': param_metrics.get("n_clusters", int(param_key) if param_key.isdigit() else None),
                    #'noise_pct': param_metrics.get("noise_pct", 0)  # 0 for non-DBSCAN
                    }
                    rows.append(row)

            df = pd.DataFrame(rows)

            if df.empty:
                raise ValueError("No metrics data found")

            # Normalize metrics to [0,1]
            df['silhouette_norm'] = self._normalize(df['silhouette_score'])

            # Davies-Bouldin: lower is better, so invert before normalization
            df["davies_bouldin_inv"] = df["davies_bouldin_score"].max() - df["davies_bouldin_score"]
            df["davies_bouldin_norm"] = self._normalize(df["davies_bouldin_inv"])

            df["calinski_harabasz_norm"] = self._normalize(df["calinski_harabasz_score"])

            df["composite_score"] = (
                df["silhouette_norm"] * weights["silhouette_score"] +
                df["davies_bouldin_norm"] * weights["davies_bouldin_score"] +
                df["calinski_harabasz_norm"] * weights["calinski_harabasz_score"]
            )

            df["rank"] = df["composite_score"].rank(ascending=False, method="first").astype(int)
            logger.info("Metrics normalization is completed...")

            return df

        except Exception as e:
            raise CustomException("Error normalizing model metrics...", sys)

    def select_best_model(self):
        try:
            logger.info("Starting the process to select best model...")
            df = self._normalize_metrics()

            best_candidates = df.loc[df["rank"] == 1]
            if best_candidates.empty:
                raise ValueError("No valid models found for selection")

            best_row = best_candidates.iloc[0]

            best_model_name = best_row["model"]
            best_params = best_row["clusters"]
            best_score = best_row["composite_score"]
            best_silhouette_score = best_row["silhouette_score"]
            best_db_score = best_row["davies_bouldin_score"]
            best_ch_score = best_row["calinski_harabasz_score"]

            logger.info(f"Best model is selected: {best_model_name}\n")
            logger.info(f"With best score of: {best_score}\n")
            logger.info(f"best silhouette score of: {best_silhouette_score} | best db score of: {best_db_score} | best ch score: {best_ch_score}\n")
            logger.info(f"and no.of clusters are: {best_params}")

            final_model_params = {
                "model": best_model_name,
                "clusters": int(best_params) if best_params.isdigit() else best_params
            }

            write_json(
                self.config.final_model_metrics,
                final_model_params
            )

            return final_model_params

        except Exception as e:
            raise CustomException("Error in finding best model...", sys)
