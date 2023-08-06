from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from plotly.graph_objs import Figure

MY_COLOR_MAP = ['green', 'aqua', 'pink', 'blue', 'red', 'black', 'yellow', 'teal', 'orange', 'grey']
obfuscated_cols = ...


def value_counts_plots(data: pd.DataFrame, rows: int = 4, cols: int = 4) -> None:
    _, ax = plt.subplots(rows, cols, sharey='row', figsize=(cols * 5, rows * 5))
    for i, feat in enumerate(data.columns[:(rows * cols)]):
        data[feat].value_counts().iloc[:20].plot(kind='bar', ax=ax[int(i / cols), int(i % cols)],
                                                 title='value_counts {}'.format(feat), color=MY_COLOR_MAP)


def get_most_correlated_variables(corr: pd.DataFrame, num_pairs: int = 10) -> pd.DataFrame:
    correlation_melted = pd.melt(corr.reset_index().rename(columns={"index": "var_1"}), id_vars="var_1",
                                 var_name='var_2')
    correlation_melted = correlation_melted[correlation_melted.var_1 != correlation_melted.var_2]
    correlation_melted['var_couple'] = correlation_melted[['var_1', 'var_2']].apply(
        lambda x: tuple(sorted([x[0], x[1]])), axis=1)
    correlation_melted = correlation_melted.drop_duplicates(subset='var_couple').drop(['var_couple'], axis=1)
    correlation_melted['abs_value'] = correlation_melted['value'].abs().round(3)
    return correlation_melted.sort_values(by='abs_value').tail(num_pairs).drop('abs_value', axis=1).reset_index(
        drop=True)


def plot_correlation_matrix(data: pd.DataFrame, features: List['str']):
    corr = data[features].corr()
    # return the most correlated variables
    most_correlated_variables = get_most_correlated_variables(corr, num_pairs=10)
    max_correlation = 1.25 * most_correlated_variables['value'].abs().max()
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    # Generate a custom diverging colormap
    ax.set_yticklabels(features, fontsize=18)
    ax.set_xticklabels(features, rotation='vertical', fontsize=18)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, vmax=max_correlation, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    return most_correlated_variables


def plot_corr_bar_plot(data: pd.DataFrame) -> Figure:
    target_corr = data.corr()
    return target_corr.iloc[:-1, -1].plot(kind='bar', color=MY_COLOR_MAP)


def get_mose_corr_features_with_target(data: pd.DataFrame, target_col: str) -> pd.DataFrame:
    corr = data.corr()
    corr_with_target = corr[[target_col]].drop(target_col, axis=0)
    corr_with_target['abs_value'] = corr_with_target.abs()
    return corr_with_target.sort_values(by='abs_value').tail(10).drop('abs_value', axis=1)


def describe_categorical_values(df: pd.DataFrame, non_interesting_columns: Optional[List['str']] = None,
                                num_values: int = 5) -> pd.DataFrame:
    values_df = pd.DataFrame()
    for i, column in enumerate(df.columns):
        if non_interesting_columns is not None and column in non_interesting_columns:
            continue
        top_values0 = [f"{x}: {int(round(100 * y / len(df)))}%"
                       for x, y in zip(df[column].value_counts(dropna=False).head(num_values).index,
                                       df[column].value_counts(dropna=False).head(num_values).values)]
        if len(top_values0) < num_values:
            top_values = [None] * num_values
            top_values[:len(top_values0)] = top_values0
        else:
            top_values = top_values0
        values_df[column] = top_values
    return values_df.T
