import os
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func
from data_preprocess import data_load, data_clean
import custom_functions as cf

def plot_heatmap(df, title='title', annot=True, fmt='.1f'):
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.heatmap(df, annot=annot, fmt=fmt, ax=ax, cmap='twilight_shifted')
    # fig, ax = plt.subplots(1, 2, figsize=(15, 5), sharex='col', gridspec_kw={'width_ratios': [100, 5]})
    # sns.heatmap(df, annot=annot, fmt=fmt, ax=ax[0], cbar_ax=ax[1], cmap='twilight_shifted')
    ax.axes.set_title(title)
    plt.tight_layout()
    return fig, ax

def plot_heatmap_and_line(df_heat, x_line, y_line, df_line=None, title1='title1', title2='title2', annot=True, fmt='.1f'):
    fig, ax = plt.subplots(2, 2, figsize=(15, 7), sharex='col', gridspec_kw={'width_ratios': [100, 5], 'height_ratios': [3, 1]})
    ax[1, 1].remove()  # remove unused axis

    # heatmap
    heat = sns.heatmap(df_heat, annot=annot, fmt=fmt, ax=ax[0, 0], cbar_ax=ax[0, 1], cmap='twilight_shifted')
    ax[0, 0].set_title(title1)

    width = heat.get_xticks()[1] - heat.get_xticks()[0]
    new_ax = heat.get_xticks() - 0.5 * width
    heat.set_xticks(new_ax)

    # line plot
    if df_line:
        line = sns.lineplot(data=df_line, x=x_line, y=y_line, ax=ax[1, 0])
    else:
        line = sns.lineplot(x=x_line, y=y_line, ax=ax[1, 0])
    ax[1, 0].set_title(title2)
    # heat.axes.set_title(title)
    plt.tight_layout(pad=5)

    return fig, ax

def plot_line(df, title='title'):
    fig, ax = plt.subplots(figsize=(8, 4))
    df.plot(title=title, fontsize=8, ax=ax)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    return fig, ax

def plot_bar(df, title='title', stacked='False'):
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot.bar(title=title, fontsize=8, ax=ax, stacked=stacked)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    return fig, ax