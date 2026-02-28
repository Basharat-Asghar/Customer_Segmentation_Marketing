import os
import sys
import yaml
import joblib
import json
import shutil
from typing import Any
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.exception import CustomException


logger = get_logger(__name__)


# --------------------------------------------------
# YAML Utilities
# --------------------------------------------------

def read_yaml(file_path: Path) -> dict:
    """
    Read YAML file and return content as dictionary.
    """

    try:
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)

        logger.info(f"YAML file loaded: {file_path}")
        return content

    except Exception as e:
        raise CustomException("Failed to read YAML file", sys) from e


def write_yaml(file_path: Path, data: dict) -> None:
    """
    Write dictionary data to YAML file.
    """

    try:
        with open(file_path, "w") as f:
            yaml.safe_dump(data, f)

        logger.info(f"YAML file written: {file_path}")

    except Exception as e:
        raise CustomException("Failed to write YAML file", sys) from e


# --------------------------------------------------
# JSON Utilities
# --------------------------------------------------

def read_json(file_path: Path) -> dict:
    """
    Read JSON file and return dictionary.
    """

    try:
        with open(file_path, "r") as f:
            content = json.load(f)

        logger.info(f"JSON file loaded: {file_path}")
        return content

    except Exception as e:
        raise CustomException("Failed to read JSON file", sys) from e


def write_json(file_path: Path, data: dict) -> None:
    """
    Write dictionary to JSON file.
    """

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"JSON file written: {file_path}")

    except Exception as e:
        raise CustomException("Failed to write JSON file", sys) from e


# --------------------------------------------------
# Directory Utilities
# --------------------------------------------------

def create_directories(path_list: list) -> None:
    """
    Create multiple directories.
    """

    try:
        for path in path_list:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: {path}")

    except Exception as e:
        raise CustomException("Failed to create directories", sys) from e


# --------------------------------------------------
# Object Serialization (Model Saving)
# --------------------------------------------------

def save_object(file_path: Path, obj: Any) -> None:
    """
    Save Python object using dill.
    """

    try:
        file_path = Path(file_path)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as f:
            joblib.dump(obj, f)

        logger.info(f"Object saved: {file_path}")

    except Exception as e:
        raise CustomException("Failed to save object", sys) from e


def load_object(file_path: Path) -> Any:
    """
    Load Python object using dill.
    """

    try:
        with open(file_path, "rb") as f:
            obj = joblib.load(f)

        logger.info(f"Object loaded: {file_path}")
        return obj

    except Exception as e:
        raise CustomException("Failed to load object", sys) from e


# --------------------------------------------------
# File Utilities
# --------------------------------------------------

def get_file_size(file_path: Path) -> float:
    """
    Get file size in MB.
    """

    try:
        size = os.path.getsize(file_path) / (1024 * 1024)
        return round(size, 3)

    except Exception as e:
        raise CustomException("Failed to get file size", sys) from e


def remove_file(file_path: Path) -> None:
    """
    Delete file safely.
    """

    try:
        file_path = Path(file_path)

        if file_path.exists():
            file_path.unlink()
            logger.info(f"File removed: {file_path}")

    except Exception as e:
        raise CustomException("Failed to remove file", sys) from e


# --------------------------------------------------
# Folder Utilities
# --------------------------------------------------

def remove_directory(dir_path: Path) -> None:
    """
    Delete directory recursively.
    """

    try:
        dir_path = Path(dir_path)

        if dir_path.exists():
            shutil.rmtree(dir_path)
            logger.info(f"Directory removed: {dir_path}")

    except Exception as e:
        raise CustomException("Failed to remove directory", sys) from e