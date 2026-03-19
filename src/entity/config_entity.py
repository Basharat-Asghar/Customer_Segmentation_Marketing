from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    db_table: str
    raw_data_path: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    valid_data_path: Path
    report_file_path: Path
    all_schema: dict

@dataclass(frozen=True)
class DataCleaningConfig:
    root_dir: Path
    cleaned_data_path: Path
    report_file_path: Path
    duplicate_strategy: str
    missing_value_strategy: str
    missing_columns: list

@dataclass(frozen=True)
class FeatureEngineeringConfig:
    root_dir: Path
    featured_data_path: Path
    log_transform_columns: list
    engagement_bins: list
    engagement_labels: list
    clv_bins: list
    clv_labels: list

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    transformed_data_path: Path
    scaler: str
    preprocessor_path: Path
    clustering_features: list

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    metrics_path: Path
    clustering_features: list
    max_k: int
    kmeans: dict
    agglomerative: dict
    gmm: dict
    dbscan: dict