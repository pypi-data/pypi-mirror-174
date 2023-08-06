from typing import Optional

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def _create_ctr_df(df: pd.DataFrame, feature: str, target_col='conversion'):
    topk = df[(df[feature].isin((df[feature].value_counts() / len(df)).index))]
    topk_click = topk[topk[target_col] == 1]
    df = topk[[feature, target_col]].groupby([feature]).size().reset_index()
    df = df.rename(columns={0: 'impressions'})
    topk_click_index = topk_click[[feature, target_col]].groupby([feature]).groups.keys()
    df = df[df[feature].isin(topk_click_index)]
    df['clicks'] = topk_click[[feature, target_col]].groupby([feature]).size().values
    df['CTR'] = df['clicks'] / df['impressions'] * 100
    return df


def plot_top_ctr(df: pd.DataFrame, feature: str, rank: int, target_col='conversion'):
    df = _create_ctr_df(df, feature, target_col)
    sort_site = df.sort_values(by='CTR', ascending=False)[feature][0:rank].tolist()
    plt.figure(figsize=(12, 6))
    sns.barplot(y='CTR', x=feature, data=df, order=sort_site)
    plt.xticks(rotation=70)
    plt.tight_layout()
    plt.title(f'Top {rank} CTR by {feature}')


def plot_top_hist(df: pd.DataFrame, feature: str, rank: int, target_col='conversion'):
    topk = df[(df[feature].isin((df[feature].value_counts() / len(df))[0:rank].index))]
    topk_click = topk[topk[target_col] == 1]
    topk_click.groupby([feature, target_col]).size().unstack().plot(kind='bar', figsize=(12, 6),
                                                                    title=f'Top {rank} {feature} histogram')


def explore_feature(df: pd.DataFrame, feature: str, rank: Optional[int] = None, target_col: str = 'conversion'):
    print(f"There are {df[feature].nunique()} {feature} in the data set")
    if rank is None:
        rank = df[feature].nunique()
    print(f'The top-{rank} {feature} that have the most impressions:')
    print((df[feature].value_counts() / len(df))[0:rank])
    print('*' * 50)
    top10_ids = (df[feature].value_counts() / len(df))[0:rank].index
    click_avg_list = []
    for i in top10_ids:
        click_avg = df.loc[np.where((df[feature] == i))][target_col].mean()
        click_avg_list.append(click_avg)
        print(f"for {feature} value: {i},  click through rate: {click_avg}")
    print('*' * 50)
    plot_top_hist(df, feature, rank)
    plot_top_ctr(df, feature, rank)


def feature_ctr_std(df: pd.DataFrame, feature: str, target_col: str = 'conversion') -> float:
    ctr_df = _create_ctr_df(df, feature, target_col)
    return ctr_df['CTR'].std()


def feature_ctr_diff(df: pd.DataFrame, feature: str, target_col: str = 'conversion') -> float:
    ctr_df = _create_ctr_df(df, feature, target_col)
    return ctr_df['CTR'].max() - ctr_df['CTR'].min()
