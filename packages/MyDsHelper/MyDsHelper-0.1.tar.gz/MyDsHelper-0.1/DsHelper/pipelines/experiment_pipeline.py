import os
from typing import Any, List, Tuple, Optional

import numpy as np
import pandas as pd
import wandb
from deepchecks.tabular import Dataset
from sklearn.model_selection import KFold

from DsHelper.common.time_decorator import timeit
from DsHelper.configs.config import WANDB_BASE_URL, WANDB_API_KEY
from DsHelper.dataset_creator.base_dataset_creator import BaseDatasetCreator
from DsHelper.pipelines.base_pipeline import BasePipeline
from DsHelper.pipelines.pipeline_utils import create_df, AGG_FUNCTIONS, preprocess_df, validate_dataset, \
    validate_train_test_split, fit_model, validate_fitted_model, get_model_results_from_suite
from DsHelper.processing.base_preprocessor import BasePreProcessor


class ExperimentPipeline(BasePipeline):
    def __init__(self, dataset_creator: BaseDatasetCreator, pre_processor: BasePreProcessor,
                 model: Any, data_source: str, wandb_project: str, wandb_entity: str, split_ratio: float = 0.2):
        self.split_ratio = split_ratio
        self.wandb_project = wandb_project
        self.wandb_entity = wandb_entity
        super().__init__(dataset_creator, pre_processor, model, data_source)

    @staticmethod
    def log_aggregated_suite_performance_results(result_list: List[pd.DataFrame]) -> None:
        result_df = pd.concat(result_list).rest_index(drop=True)
        grouped_df = result_df.groupby(['Dataset', 'Metric', 'Class']).agg({'Value': AGG_FUNCTIONS})
        metrics = {}
        for idx in range(grouped_df.shape[0]):
            base_key_name = '-'.join(map(str, grouped_df.index[idx]))
            for func_idx, func in enumerate(AGG_FUNCTIONS):
                key_name = f'{base_key_name}-{func}'
                metrics[key_name] = grouped_df.iloc[idx].values[func_idx]
        for metric_name, metric_val in metrics.items():
            wandb.run.summary[metric_name] = metric_val
        wandb.log({'Metrics': wandb.Table(dataframe=result_df)})

    @timeit
    def create_train_test_split(self, df: pd.DataFrame, train_idx: np.ndarry, test_idx: np.ndarry,
                                target_col: str, cols_for_model: List[str], cat_features: Optional[List[str]]) -> \
            Tuple[Dataset, Dataset]:
        if cat_features is None:
            cat_features = []
        print('Splitting train-test')
        train = df.iloc[train_idx]
        test = df.iloc[test_idx]
        train_ds = Dataset(train[cols_for_model], label=target_col, cat_features=cat_features)
        test_ds = Dataset(test[cols_for_model], label=target_col, cat_features=cat_features)
        return train_ds, test_ds

    @timeit
    def evaluate_model(self, train: Dataset, test: Dataset, fitted_model: Any, split_number: int) -> pd.DataFrame:
        print('Evaluating model')
        model_suite_result = validate_fitted_model(train, test, fitted_model, split_number)
        return get_model_results_from_suite(model_suite_result, split_number)

    def run_pipeline(self, str_cols: List[str], target_col: str, cols_for_model: List[str],
                     cat_features: Optional[List[str]], time_col: Optional[str]) -> None:
        os.environ['WANDB_BASE_URL'] = WANDB_BASE_URL
        os.environ['WANDB_API_KEY'] = WANDB_API_KEY
        with wandb.init(project=self.wandb_project, entity=self.wandb_entity) as wb_run:
            dataset = create_df(dataset_creator=self.dataset_creator, data_source=self.data_source)
            process_dataset = preprocess_df(dataset, self.pre_processor)
            try:
                validate_dataset(process_dataset, cat_features=str_cols, datetime_name=time_col, label=target_col)
            except AssertionError as e:
                print(f'There were issues with validation of the dataset.\n {e}')
            k_fold = KFold()
            model_results = []
            for split_number, (train_indices, test_indices) in enumerate(
                    k_fold.split(process_dataset, y=process_dataset[target_col])):
                try:
                    train, test = self.create_train_test_split(process_dataset, train_indices, test_indices, target_col,
                                                               cols_for_model, cat_features)
                except AssertionError:
                    continue
                try:
                    validate_train_test_split(train, test, split_number=split_number)
                except AssertionError as e:
                    print(f'There were issues with validation of the train-test split.\n {e}')
                model = fit_model(train, target_col, model)
                model_results.append((self.evaluate_model(train, test, model, split_number)))
            self.log_aggregated_suite_performance_results(model_results)
