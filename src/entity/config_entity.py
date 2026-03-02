from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    db_table: str
    raw_data_path: Path