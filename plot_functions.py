# This module contains various plot functions in order to visualize analysis results

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from cycler import cycler

def init_plot_settings(color):
    '''
    sets matplotlib rc parameters valid for all plots
    :param color: input list for desired default color cycle
    :return:
    '''
    # customize rc parameters:
    # https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py#L14
    # https://matplotlib.org/3.1.0/gallery/color/named_colors.html

    sns.set_context("paper", rc={"font.size": 8, "axes.titlesize": 12, "axes.labelsize": 8, "xtick.labelsize": 8,
                                 "ytick.labelsize": 8})
    sns.color_palette("icefire", as_cmap=True)
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=color)
    mpl.rcParams['font.size'] = 8
    mpl.rcParams['legend.fontsize'] = 10
    mpl.rcParams['figure.titlesize'] = 12
    return

def color_cycles():
    '''
    defines some color cycles for plots
    :return: default, color1, color2, color3 - lists of HMTL colors
    '''
    color1 = ['#68C469','#68C497','#68C3C4','#6895C4','#6968C4','#9768C4']
    color2 = ['#B468C4','#C468BD','#C468A6','#C4688F','#C46878','#C46F68']
    color3 = ['#C8AC4F','#C6C84F','#A8C84F','#89C84F','#4FC84F','#4FC86D']
    default = ['black', 'grey', 'darkorange', 'red', 'lightcoral', 'gold', 'darkred', 'greenyellow', 'sandybrown',
               'darkgreen', 'lightsteelblue', 'limegreen', 'turquoise', 'blue', 'teal', 'mediumpurple', 'fuchsia',
               'deepskyblue', 'mediumvioletred', 'darkgoldenrod']
    return default, color1, color2, color3

def plot_heatmap(df, title='title', filename='heatmap', annot=True, fmt='.1f', figsize=(15, 7), center=None):
    '''
    plots heatmap of a given pandas dataframe and saves it as PNG file
    :param df: pandas dataframe
    :param title: plot title
    :param filename: filename for PNG
    :param annot: annotate values in the heatmap
    :param fmt: format the display of values
    :param figsize: plot size
    :param center: reference heatmap colormap
    :return: figure and axis object
    '''
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=annot, annot_kws={'rotation': 90}, fmt=fmt, ax=ax, cmap='twilight_shifted', center=center)
    ax.axes.set_title(title)
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_heatmap_and_line(df_heat, x_line, y_line, df_line=None, title1='title1', title2='title2', filename='heatmap_line', figsize=(15, 10),  annot=True, fmt='.1f'):
    '''
    plots heatmap of a given pandas dataframe alog with a line plot and saves it as PNG file
    :param df_heat: pandas dataframe for heatmap
    :param x_line: x value for line plot
    :param y_line: y value for line plot
    :param df_line: pandas dataframe for line plot
    :param title1: title heatmap
    :param title2: title line plot
    :param filename: filename for PNG
    :param figsize: plot size
    :param annot: annotate values in the heatmap
    :param fmt: format the display of values
    :return: figure and axis object
    '''
    fig, ax = plt.subplots(2, 2, figsize=figsize, sharex='col', gridspec_kw={'width_ratios': [100, 5], 'height_ratios': [3, 1]})
    ax[1, 1].remove()  # remove unused axis

    # heatmap
    heat = sns.heatmap(df_heat, annot=annot, annot_kws={'rotation': 90}, fmt=fmt, ax=ax[0, 0], cbar_ax=ax[0, 1], cmap='twilight_shifted')
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

def plot_line(df, title='title', xlabel='x', ylabel='y', linecolor='black', filename='line_plot'):
    '''
    makes a simple line plot from the columns of a given pandas dataframe
    :param df: pandas dataframe with columns to plot
    :param title: plot title
    :param xlabel: x axis label
    :param ylabel: y axis label
    :param linecolor: color of the plotted line
    :param filename: filename for PNG
    :return: figure and axis object
    '''
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot(title=title, fontsize=10, ax=ax, color=linecolor)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_line_multi(df1, df2, title1='title', title2='title', xlabels=['x', 'x'], ylabels=['y', 'y'], linecolor='black', filename='line_plot_multi'):
    '''
    makes two simple line plots from the columns of two given pandas dataframe next to each other
    :param df1: pandas dataframe with columns to plot on the left side
    :param df2: pandas dataframe with columns to plot on the right side
    :param title1: plot title left
    :param title2: plot title right
    :param xlabels: x axis labels ['left', 'right']
    :param ylabels: y axis labels  ['left', 'right']
    :param linecolor: color of the plotted lines
    :param filename: filename for PNG
    :return: figure and axis object
    '''
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    df1.plot(title=title1, fontsize=10, ax=axes[0], color=linecolor)
    df2.plot(title=title2, fontsize=10, ax=axes[1], color=linecolor)

    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
    axes[0].set_xlabel(xlabels[0], fontsize=10)
    axes[0].set_ylabel(ylabels[0], fontsize=10)

    axes[1].legend(loc='upper left', bbox_to_anchor=(1, 1))
    axes[1].set_xlabel(xlabels[1], fontsize=10)
    axes[1].set_ylabel(ylabels[1], fontsize=10)

    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, axes

def plot_line_fill(df, y1, y2, title='title', xlabel='x', ylabel='y', linecolor='black', fillcolor='blue', filename='line_plot_fill'):
    '''
    makes a simple line plot from the columns of a given pandas dataframe and fills the area between two specified y-values
    :param df: pandas dataframe with columns to plot
    :param y1: value 1 for colorfill
    :param y2: value 2 for colorfill
    :param title: plot title
    :param xlabel: x axis label
    :param ylabel: y axis label
    :param linecolor: color of the plotted line
    :param fillcolor: color of the filled area between y1 and y2
    :param filename: filename for PNG
    :return: figure and axis object
    '''
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot(title=title, fontsize=10, ax=ax, color=linecolor)
    ax.fill_between(df.index, y1, y2, color=fillcolor, alpha=0.1)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

def plot_bar(df, title='title', xlabel='x', ylabel='y', filename='bar_chart', stacked=False, color='black', percentage=False):
    '''
    makes a simple bar plot from the columns of a given pandas dataframe
    :param df: pandas dataframe with columns to plot
    :param title: plot title
    :param xlabel: x axis label
    :param ylabel: y axis label
    :param filename: filename for PNG
    :param stacked: plot stacked bars
    :param color: color of the plotted bars
    :param percentage: convert parts-of-a-whole to percentages (*100)
    :return: figure and axis object
    '''
    if percentage == True:
        df = df*100
    fig, ax = plt.subplots(figsize=(15, 6))
    df.plot.bar(title=title, fontsize=8, ax=ax, stacked=stacked, color=color, grid=False)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    fig.savefig(f"results/{filename}.png")
    return fig, ax

# def plot_pie_chart(df, column, title='pie_chart', filename='pie_chart', colors=['#3EA607', '#5F9343', '#868686', '#93435F', '#A6073E']):
#     series = df[column].dropna()
#     pie, ax = plt.subplots(figsize=(15, 5))
#     plt.pie(x=series, autopct="%1.1f%%", explode= [0.02]*series.shape[0], labels=series.keys(), colors=colors)
#     plt.title(title, fontsize=12)
#     plt.tight_layout()
#     pie.savefig(f"results/{filename}.png")
#     return pie, ax
#
# def horizontal_bars_simple(df, title='', color=['#6198A2','#A26B61'], filename='hbar_chart', percentage=True):
#     if percentage == True:
#         df = df*100
#     ax = df.plot.barh(title=title, grid=True, color=color, figsize=(15, 5))
#     fig = ax.get_figure()
#     plt.tight_layout()
#     fig.savefig(f"results/{filename}.png")
#     return fig, ax