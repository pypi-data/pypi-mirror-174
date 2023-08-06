from abc import abstractmethod
from typing import Any, List, Optional

from DsHelper.dataset_creator.base_dataset_creator import BaseDatasetCreator
from DsHelper.processing.base_preprocessor import BasePreProcessor


class BasePipeline:
    def __init__(self, dataset_creator: BaseDatasetCreator, pre_processor: BasePreProcessor,
                 model: Any, data_source: str):
        self.dataset_creator = dataset_creator
        self.pre_processor = pre_processor
        self.model = model
        self.data_source = data_source

    @abstractmethod
    def run_pipeline(self, str_cols: List[str], target_col: str, cols_for_model: List[str],
                     cat_features: Optional[List[str]], time_col: Optional[str]) -> None:
        raise NotImplementedError
