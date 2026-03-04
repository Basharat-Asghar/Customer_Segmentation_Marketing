import pandas as pd
import sys
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.entity.config_entity import DataCleaningConfig

logger = get_logger(__name__)

class DataCleaner:
    def __init__(self, config: DataCleaningConfig):
        self.config = config

    def clean(self, validated_data_path: str):
        """
        Apply all cleaning steps to the raw DataFrame.

        Steps (in order):
        1. Drop exact duplicate rows.
        2. Impute missing values per config strategy.
        3. Flag edge-case rows (CLV=0, minutes_watched=0).

        Parameters
        ----------
        validated_data_path : str
        Path to the validated CSV dataset.

        Returns
        -------
        pd.DataFrame — cleaned dataset.
        """

        try:
            df = pd.read_csv(validated_data_path)
            df_out = df.copy()
            initial_len = len(df_out)
            logger.info(f"Starting data cleaning process with {initial_len} rows...")

            # ── Step 1: Drop duplicates ───────────────────────────────────────────────
            if self.config.duplicate_strategy == "drop":
                df_out = df_out.drop_duplicates()
            elif self.config.duplicate_strategy == "keep_first":
                df_out = df_out.drop_duplicates(keep='first')
            elif self.config.duplicate_strategy == "keep_last":
                df_out = df_out.drop_duplicates(keep='last')

            n_dropped = initial_len - len(df_out)
            logger.info(f"Duplicates removed: {n_dropped} rows dropped.")

            # ── Step 2: Missing value imputation ─────────────────────────────────────
            missing_cols = self.config.missing_columns
            missing_strategy = self.config.missing_value_strategy

            for col in missing_cols:
                '''
                if col not in df_out.columns:
                    continue
                '''
                n_missing = df_out[col].isnull().sum()
                if n_missing == 0:
                    continue

                if missing_strategy == 'median':
                    fill_val = df_out[col].median()
                elif missing_strategy == 'mean':
                    fill_val = df_out[col].mean()
                elif missing_strategy == 'drop':
                    df_out = df_out.dropna(subset=[col])
                    logger.info(f"Dropped {n_missing} rows with missing '{col}'")
                    continue

                df_out[col] = df_out[col].fillna(fill_val)
                logger.info(f"Imputed {n_missing} missing values in '{col}' with {missing_strategy} ({fill_val:.2f})")

            # ── Step 3: Flag edge cases (retain — never drop) ─────────────────────────
            # CLV = 0      → free-tier or refunded users (meaningful segment)
            # minutes = 0  → zero-engagement / dormant users (win-back target)

            df_out['is_free_user'] = (df_out['CLV'] == 0).astype(int)
            df_out['is_dormant_user'] = (df_out['minutes_watched'] == 0).astype(int)
            logger.info(
                f"Flagged {df_out['is_free_user'].sum()} free users, "
                f"{df_out['is_dormant_user'].sum()} zero-engagement users"
            )
            logger.info(f"Cleaning complete. Output shape: {df_out.shape}")

            df_out.to_csv(
                self.config.cleaned_data_path,
                index=False
            )
            logger.info(f"Cleaned data saved at: {self.config.cleaned_data_path}")

            return self.config.cleaned_data_path

        except Exception as e:
            raise CustomException("Error in Data Cleaning", sys)