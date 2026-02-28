# import os
import logging
from pathlib import Path

list_of_files = [
    "config/config.yaml",
    "data/raw/",
    "data/processed/",
    "artifacts/models",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data/__init__.py",
    "src/components/data/data_loader.py",
    "src/components/data/data_cleaner.py",
    "src/components/features/__init__.py",
    "src/components/features/feature_engineering.py",
    "src/components/models/__init__.py",
    "src/components/models/model_trainer.py",
    "src/components/evaluation/__init__.py",
    "src/components/evaluation/model_evaluator.py",
    "src/pipeline/__init__.py",
    "src/pipeline/train_pipeline.py",
    "src/pipeline/predict_pipeline.py",
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/exception.py",
    "src/utils/common.py",
    "src/config/__init__.py",
    "src/config/configuration.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/constants/__init__.py",
    "notebooks/",
    "templates/index.html",
    "params.yaml",
    "schema.yaml",
    "app.py",
    "requirements.txt",
    "setup.py",
]

BASE_DIR = Path(__file__).resolve().parent

for path_str in list_of_files:
    path = BASE_DIR / path_str
    # Create parent directories
    path.parent.mkdir(parents=True, exist_ok=True)

    # If path has suffix → File
    if path.suffix:
        if not path.exists():
            path.touch()
            logging.info(f"Created file: {path}")
        else:
            logging.info(f"File exists: {path}")
    # Else → Directory
    else:
        # If path exists but is file → delete it
        if path.exists() and path.is_file():
            path.unlink()
            logging.warning(f"Removed wrong file: {path}")
        
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")

'''
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists and is not empty. Skipping creation.")
'''