import os
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func

#### load, view and preprocess data ####

# general
overview = pd.read_csv("data/RKI/RKI_COVID19.csv")
casting = pd.read_csv("data/RKI/Nowcasting_Zahlen_csv.csv", sep=';')

# breakouts
breakouts = pd.read_csv("data/RKI/Ausbruchsdaten.csv", sep=';').rename(columns={'Meldewoche':'week', 'n':'num_breakouts'}).drop('sett_f', axis=1)

# cases per age
cases_age1 = pd.read_csv("data/RKI/Altersverteilung_total.csv", sep=';').drop([0], axis=0)
cases_age2 = pd.read_csv("data/RKI/Altersverteilung_perc.csv", sep=';').drop([0], axis=0)

# deaths
deaths1 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_all.csv", sep=';')\
    .rename(columns={'Sterbewoche':'week', 'Anzahl verstorbene COVID-19 Fälle':'deaths_total'})\
    .drop('Sterbejahr', axis=1)
deaths2 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_age.csv", sep=';')\
    .rename(columns={'Sterbewoche':'week',
                     'AG 0-9 Jahre':'age_0',
                     'AG 10-19 Jahre':'age_10',
                     'AG 20-29 Jahre':'age_20',
                     'AG 30-39 Jahre':'age_30',
                     'AG 40-49 Jahre':'age_40',
                     'AG 50-59 Jahre':'age_50',
                     'AG 60-69 Jahre':'age_60',
                     'AG 70-79 Jahre':'age_70',
                     'AG 80-89 Jahre':'age_80',
                     'AG 90+ Jahre':'age_90'})\
    .drop('Sterbjahr', axis=1)
deaths3 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_gender.csv", sep=';')\
    .rename(columns={'Sterbewoche':'week',
                     'Männer, AG 0-19 Jahre':'M0_19',
                     'Männer, AG 20-39 Jahre':'M20_39',
                     'Männer, AG 40-59 Jahre':'M40_59',
                     'Männer, AG 60-79 Jahre':'M60_79',
                     'Männer, AG 80+ Jahre':'M80',
                     'Frauen, AG 0-19 Jahre':'F0_19',
                     'Frauen, AG 20-39 Jahre':'F20_39',
                     'Frauen, AG 40-59 Jahre':'F40_59',
                     'Frauen, AG 60-79 Jahre':'F60_79',
                     'Frauen, AG 80+ Jahre':'F80'})\
    .drop('Sterbjahr', axis=1)
deaths = func.reduce(lambda left,right: pd.merge(left,right,on='week'), [deaths1, deaths2, deaths3])

# tests
tests1 = pd.read_csv("data/RKI/Testzahlen-gesamt.csv", sep=';')
tests2 = pd.read_csv("data/RKI/Testzahlen-rueck.csv", sep=';')

# comorbidities
comorb = pd.read_csv("data/RKI/Klinische_Aspekte.csv", sep=';')

print('done')