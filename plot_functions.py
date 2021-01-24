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
    ax.axes.set_title(title)
    plt.tight_layout()
    return fig, ax

def plot_line(df, title='title'):
    fig, ax = plt.subplots(figsize=(15, 5))
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