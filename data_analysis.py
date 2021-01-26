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
overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, clinical =\
    data_load()
# preprocess
overview, casting, breakouts, cases_age, deaths, tests, clinical =\
    data_clean(overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, clinical)

# cases info: nur Falldaten bei labordiagnostischer Bestätigung unabhängig vom klinischen Bild
# Bei der Darstellung der Neuinfektionen pro Tag wird das Meldedatum verwendet, also das Datum, an dem das GA Kenntnis von dem Fall erlangt und ihn als solchen elektronisch erfasst.




#### data overview ####
# total cases (all newly reported infections, not active cases) up to now
total_cases = overview['AnzahlFall'].sum()

# total cases per week in 2020 (with week 53 mapped to 2020)
weekly_cases = overview.loc[overview['report_date_year'] != 2021].groupby(['report_date_week']).sum()['AnzahlFall'].fillna(0)
# total cases per week per federal state in 2020
weekly_cases_per_state = overview.loc[overview['report_date_year'] != 2021].groupby(['Bundesland', 'report_date_week']).sum()['AnzahlFall'].unstack().fillna(0)

# use current population data (in 1000 units) to calculate incidences:
# https://de.statista.com/statistik/daten/studie/71085/umfrage/verteilung-der-einwohnerzahl-nach-bundeslaendern/
population_states = pd.Series(data={'Baden-Württemberg':11100, 'Bayern':13125, 'Berlin':3669,
                                  'Brandenburg':2522, 'Bremen':681, 'Hamburg':1847, 'Hessen':6288,
                                  'Mecklenburg-Vorpommern':1608, 'Niedersachsen':7994, 'Nordrhein-Westfalen':17947,
                                  'Rheinland-Pfalz':4094, 'Saarland':987, 'Sachsen':4072, 'Sachsen-Anhalt':2195,
                                  'Schleswig-Holstein':2904, 'Thüringen':2133})
total_population = population_states.sum()

# weekly incidence per federal state
weekly_incidence_per_state = (weekly_cases_per_state.div(population_states, axis=0))*100
# total weekly incidence
weekly_incidence = (weekly_cases/total_population)*100


# cases per age group over time (incidence)
age_incidence = cfunc.remove_column_substr(cases_age2.set_index('Altersgruppe'), '2020_')
# cases per age group over time (incidence) relative to overall incidence at the time
age_norm = age_incidence/age_incidence.iloc[0,:]
# cases per age group over time (total)
age_total = cfunc.remove_column_substr(cases_age1.set_index('Altersgruppe'), '2020_').drop(['Gesamt'], axis=0)



# delay in reporting (date of infection vs. date of reporting to authorities):
# 0 if no delay or unknown, negative values due to reporting delays or errors (or maybe contact persons who fell sick later)?
report_delay = overview.loc[(overview['report_delay'] >= -30) & (overview['report_delay'] <= 30)]['report_delay']



# number of breakouts in different settings
breakouts_time = breakouts.groupby('week')['num_breakouts'].sum()
breakouts_time_per_setting = breakouts.groupby(['week', 'sett_engl'])['num_breakouts'].sum().unstack()
# top 10
top_breakouts = breakouts_time_per_setting.sum().sort_values(ascending=False).index[0:10]
breakouts_time_per_setting_rel = breakouts_time_per_setting.div(breakouts_time, axis=0)

# clinical data: cases, symptoms, hospitalisation
clinical[['no_symptoms_perc', 'hospital_perc', 'deaths_perc']] = clinical[['no_symptoms_perc', 'hospital_perc', 'deaths_perc']]*100
# rates of clinical status reporting for all known cases
clinical['symptom_status_known'] = clinical['symptoms_reported']/clinical['cases_tot']
clinical['hospital_status_known'] = clinical['hospital_reported']/clinical['cases_tot']
# number of known asymptotic cases
clinical['no_symptoms_num'] = clinical['symptoms_reported']*clinical['no_symptoms_perc']/100

clinical['death_vs_tot'] = clinical['deaths_num']/clinical['cases_tot']
clinical['hospital_vs_tot'] = clinical['hospital_num']/clinical['cases_tot']
clinical['asymptomatic_vs_tot'] = clinical['no_symptoms_num']/clinical['cases_tot']

# cumulative percentages of (reported) hospitalized cases and deaths
hospitalized_cum = clinical['hospital_num'].sum()/clinical['cases_tot'].sum()
deaths_cum = clinical['deaths_num'].sum()/clinical['cases_tot'].sum()


fig, ax = pfunc.plot_line(clinical[['mean_age', 'no_symptoms_perc', 'hospital_perc', 'deaths_perc']],
                          title=f'asymptomatic cases vs. hospitalisaton and death rates \n(rates in relation to reported cases each)')
fig, ax = pfunc.plot_line(clinical[['symptom_status_known', 'hospital_status_known']],
                          title=f'reporting rates of symptoms and hospitalisation status compared to total number of known cases')
clinical_corrs = clinical[['cases_tot', 'hospital_num', 'deaths_num']].corr()





#### plots ####
# heatmap: cases per age group over time (incidence)
fig, ax = pfunc.plot_heatmap(age_incidence, title='case incidence (cases/100.000 people) per age group over time', annot=True, fmt='.1f')

# heatmap: cases per age group over time (incidence) relative to overall case incidence
# fig, ax = pfunc.plot_heatmap(age_norm.drop(['Gesamt'], axis=0), title='case incidence (cases/100.000 people) per age group over time relative to total case incidence', annot=True, fmt='.1f')
fig, ax = pfunc.plot_heatmap_and_line(age_norm.drop(['Gesamt'], axis=0),
                                      x_line=age_incidence.iloc[0].index, y_line=age_incidence.iloc[0], df_line=None,
                                      title1='case incidence (cases/100.000 people) per age group over time relative to total case incidence',
                                      title2='total case incidence over time',
                                      annot=True, fmt='.1f')

# heatmap: cases per age group over time (total)
fig, ax = pfunc.plot_heatmap(age_total, title='total cases per age group over time', annot=True, fmt='d')
# least affected group is risk group 65-75, consistently below the overall incidence:
# multiple factors could make social distancing relatively easy:
# kids and younger people with more contacts / higher mobility have moved out
# still fit enough so that there is little contact with facilities like hospitals and nursing homes
# retirement age 65, so stayathome is easily implemented
# group with the highest rate of home owners among all age groups

fig, ax = pfunc.plot_line(breakouts_time_per_setting, title='total breakouts per setting over time')
fig, ax = pfunc.plot_bar(breakouts_time_per_setting_rel, title='shares of breakouts per setting over time', stacked=True)

# heatmap: weekly cases per week per federal state in 2020
fig, ax = pfunc.plot_heatmap(weekly_cases_per_state, title='total cases per federal state over time', annot=True, fmt='.0f')
# heatmap: weekly incidence per week per federal state in 2020
fig, ax = pfunc.plot_heatmap(weekly_incidence_per_state, title='case incidence per federal state over time', annot=True, fmt='.1f')
# heatmap: weekly incidence per week per federal state in 2020 relative to overall incidence
fig, ax = pfunc.plot_heatmap_and_line(weekly_incidence_per_state,
                                      x_line=weekly_incidence.index,
                                      y_line=weekly_incidence, df_line=None,
                                      title1='case incidence (cases/100.000 people) per federal state over time relative to total case incidence',
                                      title2='total case incidence over time',
                                      annot=True, fmt='.0f')




# delay in reporting (date of infection vs. date of reporting to authorities): 0 if no delay or unknown, negative values due to reporting delays or errors (or maybe contact persons who fell sick later)?
fig = report_delay.hist(bins=61)
# report day of week
fig = overview['report_date_dayofweek'].hist(bins=7)



print('done')