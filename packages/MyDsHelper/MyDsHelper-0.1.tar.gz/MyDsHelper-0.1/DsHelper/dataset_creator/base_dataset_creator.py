from abc import abstractmethod
from typing import Dict

import pandas as pd


class BaseDatasetCreator:
    def __init__(self):
        self.dataset_builders = self.get_dataset_builders()

    @abstractmethod
    def load_dataset_from_db(self) -> pd.Dataframe:
        raise NotImplementedError

    @abstractmethod
    def load_dataset_from_path(self) -> pd.Dataframe:
        raise NotImplementedError

    @abstractmethod
    def create_dataset(self) -> pd.Dataframe:
        raise NotImplementedError

    def get_dataset_builders(self) -> Dict[str, callable]:
        return {'DB': self.load_dataset_from_db,
                'PATH': self.load_dataset_from_path,
                'CREATE': self.create_dataset}

    def get_dataset(self, source: str = 'Path') -> pd.Dataframe:
        return self.dataset_builders[source]()
