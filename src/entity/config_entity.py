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
    duplicate_strategy: str
    missing_value_strategy: str
    missing_columns: list