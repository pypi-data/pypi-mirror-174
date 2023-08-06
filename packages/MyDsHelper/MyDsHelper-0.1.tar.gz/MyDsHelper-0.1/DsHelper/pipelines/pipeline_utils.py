from typing import Any, List, Optional

from deepchecks import SuiteResult, Suite
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity
from DsHelper.common.time_decorator import timeit
from DsHelper.dataset_creator.base_dataset_creator import BaseDatasetCreator
import pandas as pd

from DsHelper.processing.base_preprocessor import BasePreProcessor

AGG_FUNCTIONS = ['mean', 'median', 'var']


@timeit
def create_df(dataset_creator: BaseDatasetCreator, data_source: str) -> pd.DataFrame:
    print(f'Getting dataset from {data_source}')
    unprocessed_dataset = dataset_creator.get_dataset(source=data_source)
    return unprocessed_dataset


@timeit
def fit_model(train: Dataset, target_col: str, model: Any) -> Any:
    print('Fitting Model')
    model.fit(train.data.drop([target_col], axis=1), train.data.target)
    return model


@timeit
def preprocess_df(unprocessed_df: pd.DataFrame, preprocessor: BasePreProcessor) -> pd.DataFrame:
    print('PreProcessing data')
    processed_df = preprocessor.pre_process(unprocessed_df)
    return processed_df


@timeit
def validate_dataset(processed_df: pd.DataFrame, cat_features: List[str] = None, label: str = None,
                     datetime_name: Optional[str] = None, log_to_wandb: bool = True) -> None:
    print('Validating dataset using data_integrity_suite')
    dataset = Dataset(processed_df, label=label, datetime_name=datetime_name, cat_features=cat_features)
    suite = data_integrity()
    suite_result = suite.run(dataset)
    if log_to_wandb:
        suite_result.to_wandb()
    assert suite_result.passed(), \
        f'{len(suite_result.get_not_passed_checks())} tests didnt "PASS,' \
        f'They are {[check.get_header() for check in suite_result.get_not_passed_checks()]}'


def _get_train_test_validation() -> Suite:
    return Suite('Train Test Validation Suite',
                 )


def _get_model_evaluations_suite() -> Suite:
    return Suite('Model Performance Suite',
                 )


@timeit
def validate_train_test_split(train_ds: Dataset, test_ds: Dataset, split_number: Optional[int],
                              log_to_wandb: bool = True) -> None:
    print('Validating train-test split using train_test_validation_suite')
    suite = _get_train_test_validation()
    if split_number:
        suite.name = f'{suite.name}: Split Number - {split_number}'
    suite_result = suite.run(train_dataset=train_ds, test_dataset=test_ds)
    if log_to_wandb:
        suite_result.to_wandb()

    assert suite_result.passed(), \
        f'{len(suite_result.get_not_passed_checks())} tests didnt "PASS,' \
        f'They are {[check.get_header() for check in suite_result.get_not_passed_checks()]}'


@timeit
def validate_fitted_model(train: Dataset, test: Dataset, model: Any, split_number: Optional[int],
                          log_to_wandb: bool = True) -> SuiteResult:
    suite = _get_model_evaluations_suite()
    if split_number:
        suite.name = f'{suite.name}: Split Number - {split_number}'
    print('Evaluating model using model_evaluation_suite')
    suite_result = suite.run(train_dataset=train, test_dataset=test, model=model)
    if log_to_wandb:
        suite_result.to_wandb()
    try:
        assert suite_result.passed(), \
            f'{len(suite_result.get_not_passed_checks())} tests didnt "PASS,' \
            f'They are {[check.get_header() for check in suite_result.get_not_passed_checks()]}'
    except AssertionError as e:
        print(f'There were problems with model validation.\n {e}')
    finally:
        return suite_result


def create_auc_results_df(metrics_results: pd.DataFrame, auc_results: dict, auc_type: str,
                          split_number: int) -> pd.DataFrame:
    if auc_type not in ['Test', 'Train']:
        raise ValueError('auc_type must be in ["Test","Train"]')
    num_classes = metrics_results.Class.nunique()
    assert num_classes == len(auc_results.keys())
    return pd.DataFrame(data={'Dataset': [auc_type] * num_classes,
                              'Class': list(metrics_results.Class.uniqe()),
                              'Metric': ['AUC'] * num_classes,
                              'Value': [v for v in auc_results.values()],
                              'Number of samples': list(
                                  metrics_results[metrics_results['Dataset'] == auc_type] \
                                      ['Number of samples'].iloc[:num_classes]),
                              'Val split': [split_number] * num_classes
                              })


def get_result_value_by_check_name(check_name: str, suite_results: SuiteResult) -> Any:
    for result in suite_results.results:
        if result.get_header() == check_name:
            return result.value
    raise ValueError(f'Check {check_name} not in suite results')


def get_model_results_from_suite(model_suite_result: SuiteResult, split_number: int) -> pd.DataFrame:
    metrics_result = get_result_value_by_check_name('Performance Report', model_suite_result)
    metrics_result['Val Split'] = split_number
    auc_train_results = get_result_value_by_check_name('ROC Report - Train Dataset', model_suite_result)
    auc_test_results = get_result_value_by_check_name('ROC Report - Test Dataset', model_suite_result)
    auc_train_df = create_auc_results_df(metrics_result, auc_train_results, 'Train', split_number)
    auc_test_df = create_auc_results_df(metrics_result, auc_test_results, 'Test', split_number)
    return pd.concat([metrics_result, auc_train_df, auc_test_df])
