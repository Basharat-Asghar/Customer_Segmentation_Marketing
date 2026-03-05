import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
import sys

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import save_object, write_json

logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def _load_data(self, data_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(data_path)

            return df

        except Exception as e:
            raise CustomException("Error in loading data for model training", sys)
        
    def _find_best_k(self, X):
        try:
            best_k = 2,
            best_score = -1

            inertia_values = []
            silhouette_scores = {}

            for k in range(2, self.config.max_k + 1):
                model = KMeans(
                    n_clusters=k,
                    init=self.config.init,
                    n_init=self.config.n_init,
                    max_iter=self.config.max_iter,
                    random_state=self.config.random_state
                )

                cluster_labels = model.fit_predict(X)

                inertia_values.append(model.inertia_)
                score = silhouette_score(X, cluster_labels)
                silhouette_scores[k] = score

                logger.info(f"K: {k}, Inertia: {model.inertia_}, Silhouette Score: {score}")

                if score > best_score:
                    best_k = k
                    best_score = score

            return best_k, inertia_values, silhouette_scores

        except Exception as e:
            raise CustomException("Error in finding best k for KMeans", sys)
        
    def train_model(self, data_path: str):
        try:
            logger.info("Loading data for model training...")
            df = self._load_data(data_path)

            X = df[self.config.clustering_features].values

            logger.info("Finding the best number of clusters (k) using silhouette score...")
            best_k, inertia_values, silhouette_scores = self._find_best_k(X)

            logger.info(f"Best k found: {best_k} with silhouette score: {silhouette_scores[best_k]}")

            logger.info("Training KMeans model with best k...")
            final_model = KMeans(
                n_clusters=best_k,
                init=self.config.init,
                n_init=self.config.n_init,
                max_iter=self.config.max_iter,
                random_state=self.config.random_state
            )

            final_model.fit(X)
            cluster_labels = final_model.labels_
            df['cluster'] = cluster_labels

            df.to_csv(
                self.config.clustered_data_path,
                index=False
            )
            logger.info(f"Clustered data saved to: {self.config.clustered_data_path}")

            save_object(
                self.config.model_path,
                final_model
            )
            logger.info(f"Saved trained model to: {self.config.model_path}")

            metrics = {
                "best_k": best_k,
                "inertia": inertia_values,
                "silhouette_scores": silhouette_scores
            }
            write_json(
                self.config.metrics_path,
                metrics
            )
            logger.info(f"Metrics saved to: {self.config.metrics_path}")

            return self.config.model_path, df

        except Exception as e:
            raise CustomException("Error in training model", sys)
