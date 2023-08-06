import os
import pickle
from typing import Any, List, Optional

from deepchecks import Dataset

from DsHelper.common.time_decorator import timeit
from DsHelper.configs.config import PROD_MODEL_FILE_PATH
from DsHelper.pipelines.base_pipeline import BasePipeline
from DsHelper.pipelines.pipeline_utils import create_df, preprocess_df, validate_dataset, fit_model


@timeit
def save_model(model: Any, model_dir: Optional[str] = None, model_dave_path: Optional[str] = None):
    os.makedirs(model_dir, exist_ok=True)
    print('Saving model')
    model_dave_path = model_dave_path or str(PROD_MODEL_FILE_PATH)
    try:
        model.save_model(model_dave_path)
    except (NameError, NotImplementedError):
        print('Saving using pickle')
        with open(model_dave_path, "w+b") as file:
            pickle.dump(model, file)


class TrainingPipeline(BasePipeline):
    def run_pipeline(self, target_col: str, cat_features: List[str], cols_for_model: List[str], model: Any,
                     time_col: Optional[str] = None):
        df = create_df(self.dataset_creator, self.data_source)
        processed_df = preprocess_df(df, self.pre_processor)
        processed_df = processed_df[cols_for_model]
        try:
            validate_dataset(processed_df, cat_features, target_col, log_to_wandb=False)
        except AssertionError as e:
            print(f'There were issues with validation of the dataset.\n {e}')
        ds = Dataset(processed_df, cat_features=cat_features, label=target_col)
        model = fit_model(ds, target_col, model)
        save_model(model)
