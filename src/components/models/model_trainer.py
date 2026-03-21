import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
import sys

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import write_json, read_json, save_object

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
        
    def _compute_clustering_metrics(self, X, labels) -> dict:
        # Compute all clustering evaluation metrics. Returns empty dict if only 1 cluster.
        if len(set(labels)) < 1:
            return {}
        
        '''
        # Exclude noise points (DBSCAN label = -1) from metric computation
        if -1 in labels:
            mask = labels != -1
            X = X[mask]
            labels = labels[mask]
        '''
        
        # Compute clustering metrics
        silhouette = silhouette_score(X, labels)
        davies_bouldin = davies_bouldin_score(X, labels)
        calinski_harabasz = calinski_harabasz_score(X, labels)

        return {
            "silhouette": silhouette,
            "davies_bouldin": davies_bouldin,
            "calinski_harabasz": calinski_harabasz
        }

    def train_kmeans(self, X):
        try:
            logger.info("Training KMeans model...")
            kmeans_metrics = {}

            for k in range(2, self.config.max_k + 1):
                kmeans = KMeans(
                    n_clusters=k,
                    init=self.config.kmeans.init,
                    n_init=self.config.kmeans.n_init,
                    max_iter=self.config.kmeans.max_iter,
                    random_state=self.config.kmeans.random_state
                )

                labels = kmeans.fit_predict(X)
                metrics = self._compute_clustering_metrics(X, labels)
                kmeans_metrics[k] = metrics
            logger.info(f"KMeans training completed. Metrics for different k: {kmeans_metrics}")

            return kmeans_metrics

        except Exception as e:
            raise CustomException("Error in training KMeans model", sys)
        
    def train_agglomerative(self, X):
        try:
            logger.info("Training Agglomerative Clustering model...")
            agglomerative_metrics = {}

            for k in range(2, self.config.max_k + 1):
                aggglomerative = AgglomerativeClustering(
                    n_clusters=k,
                    metric=self.config.agglomerative.metric,
                    linkage=self.config.agglomerative.linkage
                )

                aggglomerative.fit(X)
                labels = aggglomerative.labels_
                metrics = self._compute_clustering_metrics(X, labels)
                agglomerative_metrics[k] = metrics
            logger.info(f"Agglomerative Clustering training completed. Metrics for different k: {agglomerative_metrics}")

            return agglomerative_metrics

        except Exception as e:
            raise CustomException("Error in training Agglomerative Clustering model", sys)
        
    def train_gmm(self, X):
        try:
            logger.info("Training Gaussian Mixture Model...")
            gmm_metrics = {}

            for k in range(2, self.config.max_k + 1):
                gmm = GaussianMixture(
                    n_components=k,
                    covariance_type=self.config.gmm.covariance_type,
                    n_init=self.config.gmm.n_init,
                    max_iter=self.config.gmm.max_iter,
                    random_state=self.config.gmm.random_state
                )

                labels = gmm.fit_predict(X)
                metrics = self._compute_clustering_metrics(X, labels)
                gmm_metrics[k] = metrics
            logger.info(f"Gaussian Mixture Model training completed. Metrics for different k: {gmm_metrics}")

            return gmm_metrics

        except Exception as e:
            raise CustomException("Error in training Gaussian Mixture Model", sys)

    '''    
    def train_dbscan(self, X):
        try:
            logger.info("Training DBSCAN model...")
            dbscan_metrics = {}

            for eps in self.config.dbscan.eps_range:
                for min_samples in self.config.dbscan.min_samples:
                    dbscan = DBSCAN(
                        eps=eps,
                        min_samples=min_samples,
                        n_jobs=-1
                    )

                    labels = dbscan.fit_predict(X)
                    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                    noise_pct = (labels == -1).mean() * 100
                    if n_clusters < 2 or n_clusters > 10 or noise_pct > 50:
                        continue

                    metrics = self._compute_clustering_metrics(X, labels)
                    metrics.update({
                        "n_clusters": n_clusters,
                        "eps": eps,
                        "min_samples": min_samples,
                        "noise_pct": noise_pct
                    })

                    dbscan_metrics[f"eps_{eps}_min_samples_{min_samples}_clusters_{n_clusters}"] = metrics
            logger.info(f"DBSCAN training completed. Metrics for different hyperparameters: {dbscan_metrics}")

            return dbscan_metrics

        except Exception as e:
            raise CustomException("Error in training DBSCAN model", sys)
    '''
        
    def train_all_models(self, data_path: str) -> dict:
        try:
            logger.info("Loading data for model training...")
            df = self._load_data(data_path)
            X = df[self.config.clustering_features].values

            kmeans_metrics = self.train_kmeans(X)
            agglomerative_metrics = self.train_agglomerative(X)
            gmm_metrics = self.train_gmm(X)
            #dbscan_metrics = self.train_dbscan(X)

            metrics = {
                "kmeans": kmeans_metrics,
                "agglomerative": agglomerative_metrics,
                "gmm": gmm_metrics,
                #"dbscan": dbscan_metrics
            }

            write_json(
                self.config.metrics_path,
                metrics
            )

            return metrics

        except Exception as e:
            raise CustomException("Error in training model", sys)

    def train_final_model(self, data_path: str):
        try:
            logger.info("Started Final Model Training...")
            df = self._load_data(data_path)
            X = df[self.config.clustering_features].values
            model_metadata = read_json(self.config.final_model_metadata)

            if model_metadata['model'] == 'kmeans':
                kmeans = KMeans(
                    n_clusters=model_metadata['clusters'],
                    init=self.config.kmeans.init,
                    n_init=self.config.kmeans.n_init,
                    max_iter=self.config.kmeans.max_iter,
                    random_state=self.config.kmeans.random_state
                )

                labels = kmeans.fit_predict(X)
                df['cluster'] = labels

                df.to_csv(
                    self.config.clustered_data_path, index=False
                )
                logger.info(f"Clustered df saved at: {self.config.clustered_data_path}")

                save_object(
                    self.config.final_model,
                    kmeans
                )
                logger.info(f"Final KMeans model saved at: {self.config.final_model}")

                return self.config.final_model

            elif model_metadata['model'] == 'agglomerative':
                aggglomerative = AgglomerativeClustering(
                    n_clusters=model_metadata['clusters'],
                    metric=self.config.agglomerative.metric,
                    linkage=self.config.agglomerative.linkage
                )
                aggglomerative.fit(X)
                labels = aggglomerative.labels_
                df['cluster'] = labels

                df.to_csv(
                    self.config.clustered_data_path, index=False
                )
                logger.info(f"Clustered df saved at: {self.config.clustered_data_path}")

                save_object(
                    self.config.final_model,
                    aggglomerative
                )
                logger.info(f"Final Agglomerative model saved at: {self.config.final_model}")

                return self.config.final_model

            elif model_metadata['model'] == 'gmm':
                gmm = GaussianMixture(
                    n_components=model_metadata['clusters'],
                    covariance_type=self.config.gmm.covariance_type,
                    n_init=self.config.gmm.n_init,
                    max_iter=self.config.gmm.max_iter,
                    random_state=self.config.gmm.random_state
                )
                labels = gmm.fit_predict(X)
                df['cluster'] = labels

                df.to_csv(
                    self.config.clustered_data_path, index=False
                )
                logger.info(f"Clustered df saved at: {self.config.clustered_data_path}")

                save_object(
                    self.config.final_model,
                    gmm
                )
                logger.info(f"Final Gaussian Mixture Model saved at: {self.config.final_model}")

                return self.config.final_model


        except Exception as e:
            raise CustomException("Failed to train final best model...")
