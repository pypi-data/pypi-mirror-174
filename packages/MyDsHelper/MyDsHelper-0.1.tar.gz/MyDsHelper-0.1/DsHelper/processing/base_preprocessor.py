from abc import abstractmethod
from typing import List, Union

import pandas as pd


def str_to_bool(s: Union[str, int]) -> bool:
    if isinstance(s, str):
        return s == 'True'
    return s == 1


class BasePreProcessor:
    def __init__(self, features_to_keep: List[str] = None):
        self.cols_to_keep = features_to_keep

    @staticmethod
    def _change_columns_to_str(df: pd.DataFrame, str_columns: List[str]) -> pd.DataFrame:
        str_cols = [col for col in str_columns if col in df]
        df[str_cols] = df[str_columns].astype(str)
        return df

    @staticmethod
    def remove_infrequent_values(df: pd.DataFrame, categorical_columns: List[str], frequency_threshold: int = 20):
        for cat_col in categorical_columns:
            col_count = df[cat_col].value_counts()
            infrequent_values = col_count[col_count < frequency_threshold].index.values
            if not col_count[col_count < 20].empty:
                print("removing values: \n{} \n".format(col_count[col_count < frequency_threshold]))
                df = df[~df[cat_col].isin(infrequent_values)]
        return df.reset_index(drop=True)

    @abstractmethod
    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_to_keep = [col for col in self.cols_to_keep if col in df]
        df = df[cols_to_keep]
        df = df.dropna(how='all', axis=1)
        return df
