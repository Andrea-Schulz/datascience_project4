import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from cycler import cycler
import functools as func
from data_preprocess import data_load, data_clean
import custom_functions as cf

def init_plot_settings():
    #### customizing rc parameters:
    # https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py#L14
    # https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    sns.set_context("paper", rc={"font.size": 6, "axes.titlesize": 12, "axes.labelsize": 6, "xtick.labelsize": 6,
                                 "ytick.labelsize": 6})
    sns.color_palette("icefire", as_cmap=True)
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['black', 'grey', 'darkorange', 'red', 'lightcoral', 'gold', 'darkred', 'greenyellow', 'sandybrown',
               'darkgreen', 'lightsteelblue', 'limegreen', 'turquoise', 'blue', 'teal', 'mediumpurple', 'fuchsia',
               'deepskyblue', 'mediumvioletred', 'darkgoldenrod'])
    mpl.rcParams['font.size'] = 6
    mpl.rcParams['legend.fontsize'] = 6
    mpl.rcParams['figure.titlesize'] = 12
    return

def color_cycles():
    color1 = ['#68C469','#68C497','#68C3C4','#6895C4','#6968C4','#9768C4']
    color2 = ['#B468C4','#C468BD','#C468A6','#C4688F','#C46878','#C46F68']
    color3 = ['#C8AC4F','#C6C84F','#A8C84F','#89C84F','#4FC84F','#4FC86D']
    return color1, color2, color3

def plot_heatmap(df, title='title', filename='heatmap', annot=True, fmt='.1f', figsize=(15, 5), center=None):
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=annot, fmt=fmt, ax=ax, cmap='twilight_shifted', center=center)
    # fig, ax = plt.subplots(1, 2, figsize=(15, 5), sharex='col', gridspec_kw={'width_ratios': [100, 5]})
    # sns.heatmap(df, annot=annot, fmt=fmt, ax=ax[0], cbar_ax=ax[1], cmap='twilight_shifted')
    ax.axes.set_title(title)
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_heatmap_and_line(df_heat, x_line, y_line, df_line=None, title1='title1', title2='title2', filename='heatmap_line', annot=True, fmt='.1f'):
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
    fig.savefig(f"results/{filename}.png")

    return fig, ax

def plot_line(df, title='title', filename='line_plot'):
    fig, ax = plt.subplots(figsize=(8, 4))
    df.plot(title=title, fontsize=8, ax=ax)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_bar(df, title='title', filename='bar_chart', stacked=False, percentage=False):
    if percentage == True:
        df = df*100
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot.bar(title=title, fontsize=8, ax=ax, stacked=stacked, grid=False)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_pie_chart(df, column, title='pie_chart', filename='pie_chart', colors=['#3EA607', '#5F9343', '#868686', '#93435F', '#A6073E']):
    series = df[column].dropna()
    pie, ax = plt.subplots(figsize=(10,4))
    plt.pie(x=series, autopct="%1.1f%%", explode= [0.02]*series.shape[0], labels=series.keys(), colors=colors)
    plt.title(title, fontsize=12)
    plt.tight_layout()
    pie.savefig(f"results/{filename}.png")
    return pie, ax

def horizontal_bars_simple(df, title='', color=['#6198A2','#A26B61'], filename='hbar_chart', percentage=True):
    if percentage == True:
        df = df*100
    ax = df.plot.barh(title=title, grid=True, color=color, figsize=(10,4))
    fig = ax.get_figure()
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax