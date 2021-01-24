import os
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
from cycler import cycler
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func
from data_preprocess import data_load, data_clean
import custom_functions as cfunc
import plot_functions as pfunc

#### customizing rc parameters:
# https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py#L14
# https://matplotlib.org/3.1.0/gallery/color/named_colors.html
sns.set_context("paper", rc={"font.size": 6, "axes.titlesize": 12, "axes.labelsize": 6, "xtick.labelsize": 6, "ytick.labelsize": 6})
sns.color_palette("icefire", as_cmap=True)
mpl.rcParams['axes.prop_cycle'] = cycler(color=['black', 'grey', 'darkorange', 'red', 'lightcoral', 'gold', 'darkred', 'greenyellow', 'sandybrown', 'darkgreen', 'lightsteelblue', 'limegreen', 'turquoise', 'blue', 'teal', 'mediumpurple', 'fuchsia', 'deepskyblue', 'mediumvioletred', 'darkgoldenrod'])
mpl.rcParams['font.size'] = 6
mpl.rcParams['legend.fontsize'] = 6
mpl.rcParams['figure.titlesize'] = 12

#### load, view and preprocess data ####
# load
overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, comorb =\
    data_load()
# preprocess
overview, casting, breakouts, cases_age, deaths, tests, comorb =\
    data_clean(overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, comorb)

#### data overview ####
total_cases = overview['AnzahlFall'].sum()

# heatmap: cases per age group over time (incidence)
age_incidence = cfunc.remove_column_substr(cases_age2.set_index('Altersgruppe'), '2020_')
fig, ax = pfunc.plot_heatmap(age_incidence, title='case incidence (cases/100.000 people) per age group over time', annot=True, fmt='.1f')

# heatmap: cases per age group over time (incidence) relative to overall incidence at the time
age_norm = age_incidence/age_incidence.iloc[0,:]
fig, ax = pfunc.plot_heatmap(age_norm, title='case incidence (cases/100.000 people) per age group over time - relative to overall incidence', annot=True, fmt='.1f')

# heatmap: cases per age group over time (total)
age_total = cfunc.remove_column_substr(cases_age1.set_index('Altersgruppe'), '2020_').drop(['Gesamt'], axis=0)
fig, ax = pfunc.plot_heatmap(age_total, title='total cases per age group over time', annot=True, fmt='d')

# number of breakouts in different settings
breakouts_time = breakouts.groupby('week')['num_breakouts'].sum()
breakouts_time_per_setting = breakouts.groupby(['week', 'sett_engl'])['num_breakouts'].sum().unstack()
bla = breakouts_time_per_setting.div(breakouts_time, axis=0)

fig, ax = pfunc.plot_line(breakouts_time_per_setting, title='total breakouts per setting over time')
fig, ax = pfunc.plot_bar(bla, title='shares of breakouts per setting over time', stacked=True)

print('done')