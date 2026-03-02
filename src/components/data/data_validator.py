import pandas as pd
import json
import yaml
import sys
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.utils.common import write_json
from src.entity.config_entity import DataValidationConfig

logger = get_logger(__name__)

class DataValidation():
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_schema(self, df: pd.DataFrame) -> dict:
        """
        Validate columns and datatypes.
        """
        report = {
            "missing_columns": [],
            "extra_columns": [],
            "datatype_mismatch": {},
            "status": True
        }

        expected_columns = self.config.all_schema

        for col in expected_columns:
            if col not in df.columns:
                report["missing_columns"].append(col)
                report['status'] = False

        for col in df.columns:
            if col not in expected_columns:
                report["extra_columns"].append(col)

        for col, dtype in expected_columns.items():
            if col in df.columns:
                actual_dtype = str(df[col].dtype)
                if actual_dtype != dtype:
                    report["datatype_mismatch"][col] = {
                        "expected": dtype,
                        "actual": actual_dtype
                    }
                    report["status"] = False

        return report
    

    def initiate_data_validation(self, raw_data_path: Path):
        try:
            logger.info("Starting Data Validtaion...")
            df = pd.read_csv(raw_data_path)

            report = self.validate_schema(df)
            write_json(self.config.report_file_path, report)

            if report["status"]:
                df.to_csv(
                    self.config.valid_data_path,
                    index=False
                )
                logger.info(f"Data Validation successful. Valid data saved at: {self.config.valid_data_path}")

                return self.config.valid_data_path
            else:
                logger.error(f"Data Validation failed. Report saved at: {self.config.report_file_path}")

        except Exception as e:
            raise CustomException("Error in Data Validation", sys)

