import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func
from data_preprocess import data_load, data_clean
import custom_functions as cfunc
import plot_functions as pfunc

#### customize plot settings and parameters

default, color1, color2, color3 = pfunc.color_cycles()
pfunc.init_plot_settings(color=default)

#### load, view and preprocess data ####
# load
overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, clinical =\
    data_load()
# preprocess
overview, casting, breakouts, cases_age, deaths, tests, clinical =\
    data_clean(overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, clinical)


#### data overview ####

# delay in reporting (date of infection vs. date of reporting to authorities):
# 0 if no delay or unknown, negative values due to reporting delays or errors (or maybe contact persons who fell sick later)?
report_delay = overview.loc[(overview['report_delay'] >= -30) & (overview['report_delay'] <= 30)]['report_delay']


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

# correlation of normalized incidences between age groups
age_groups_corr = age_norm.T.corr()



# number of breakouts in different infection settings (breakout = 2 or more related cases)
# breakouts_time = breakouts.groupby('week')['num_breakouts'].sum()
breakouts_time_per_setting = breakouts.groupby(['week', 'sett_engl'])['num_breakouts'].sum().unstack().fillna(0)
# top 10
top_breakouts = breakouts_time_per_setting.sum().sort_values(ascending=False).index[0:10]
breakouts_time_per_setting_rel = (breakouts_time_per_setting.div(breakouts_time_per_setting.sum(axis=1), axis=0)).fillna(0)

# calculate weekly cases with unknown infection setting in 2020 as: single_unknown_cases = total_cases - sum(cases_from_breakouts)
unknown_cases = pd.concat([weekly_cases, breakouts_time_per_setting.sum(axis=1).rename('weekly_sum_breakouts')], axis=1).fillna(0).loc[:53, :]
unknown_cases['weekly_single_unknown_cases'] = unknown_cases['AnzahlFall'] - unknown_cases['weekly_sum_breakouts']
unknown_cases['weekly_sum_breakouts_perc'] = unknown_cases['weekly_sum_breakouts']/unknown_cases['AnzahlFall']
# mean percentage of cases that are allocated to a breakout setting
unknown_cases['weekly_sum_breakouts_perc'].loc[9:].mean()

# add single unknown cases to breakout table
breakouts_time_per_setting2 = breakouts_time_per_setting.copy(deep=True)
breakouts_time_per_setting2['Unknown single'] = unknown_cases['weekly_single_unknown_cases'].loc[9:]
breakouts_time_per_setting2['Unknown total'] = breakouts_time_per_setting2['Unknown single'] + breakouts_time_per_setting2['Unknown']

# calculate new numbers and percentages of breakouts
breakouts_time_per_setting_rel2 = (breakouts_time_per_setting2.drop(['Unknown single', 'Unknown'], axis=1)
                                   .div(breakouts_time_per_setting2.drop(['Unknown single', 'Unknown'], axis=1).sum(axis=1), axis=0)).fillna(0)

# correlations
age_norm_trans = age_norm.rename(columns={'2021_1': '54'}).T
age_norm_trans.index = age_norm_trans.index.astype('int').rename('week')
age_vs_breakouts = pd.concat([breakouts_time_per_setting2, age_norm_trans], axis=1)
age_vs_breakouts_summer = pd.concat([breakouts_time_per_setting2, age_norm_trans], axis=1).loc[18:44, :]
# correlation age vs breakouts: take upper right side of correlation matrix
age_vs_breakouts_corr = age_vs_breakouts.corr().loc[:'Work place', '90+':]
# age_vs_breakouts_corr_summer = age_vs_breakouts_summer.corr().loc[:'Work place', '90+':]


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
clinical_corrs = clinical[['cases_tot', 'hospital_num', 'deaths_num']].corr()


#### plots ####
# heatmap: cases per age group over time (total)
fig, ax = pfunc.plot_heatmap(age_total,
                             title='total cases per age group over time',
                             filename='cases_total_per_age',
                             annot=True, fmt='d')
# heatmap: cases per age group over time (incidence)
fig, ax = pfunc.plot_heatmap(age_incidence,
                             title='case incidence (cases/100.000 people) per age group over time',
                             filename='incidence_age_overall',
                             annot=True, fmt='.1f')
# heatmap: cases per age group over time (incidence) relative to overall case incidence
fig, ax = pfunc.plot_heatmap_and_line(age_norm.drop(['Gesamt'], axis=0),
                                      x_line=age_incidence.iloc[0].index, y_line=age_incidence.iloc[0], df_line=None,
                                      title1='case incidence (cases/100.000 people) per age group over time - relative to total case incidence',
                                      filename='incidence_age_relative',
                                      title2='total case incidence over time',
                                      annot=True, fmt='.1f')

fig, ax = pfunc.plot_heatmap(age_groups_corr,
                             title=f'correlation of normalized incidences between age groups',
                             filename='corr_age_groups',
                             annot=True, fmt='.1f', figsize=(8,6), center=0)

# breakouts (total vs. shares)
fig, ax = pfunc.plot_line(breakouts_time_per_setting,
                          title='total number of breakouts per infection setting',
                          filename='total_breakouts')
fig, ax = pfunc.plot_bar(breakouts_time_per_setting_rel*100,
                         title='infection settings relative to total number of breakouts in percent [%]',
                         filename='shares_breakouts',
                         stacked=True)
fig, ax = pfunc.plot_bar(unknown_cases[['weekly_sum_breakouts', 'weekly_single_unknown_cases']],
                          title=f'cases attributed to a breakout vs. cases without a documented infection setting',
                          filename='unknown_cases', stacked=True)
# fig, ax = pfunc.plot_line(unknown_cases['weekly_sum_breakouts_perc'].loc[9:]*100,
#                           title=f'percentage of cases attributed to a breakout',
#                           filename='traced_cases_perc')
fig, ax = pfunc.plot_bar((breakouts_time_per_setting_rel2.reindex(sorted(breakouts_time_per_setting_rel2.columns), axis=1).loc[:53,:])*100,
                          title=f'infection settings relative to total number of cases in percent [%]',
                          filename='shares_breakouts_total', stacked=True)

fig, ax = pfunc.plot_heatmap(age_vs_breakouts_corr,
                             title=f'correlations between relative case incidence in age groups \nand number of cases allocated to breakout settings',
                             filename='corr_age_breakouts',
                             annot=True, fmt='.1f', figsize=(8,6), center=0)
# fig, ax = pfunc.plot_heatmap(age_vs_breakouts_corr_summer,,
#                              title=f'correlations between number of cases per age \nand number of cases allocated to breakout settings - in summer only',
#                              filename='corr_age_breakouts',
#                              annot=True, fmt='.1f', figsize=(8,6), center=0)


# heatmap: weekly cases per week per federal state in 2020
fig, ax = pfunc.plot_heatmap(weekly_cases_per_state,
                             title='total cases per federal state over time',
                             filename='cases_total_per_state',
                             annot=True, fmt='.0f')
# heatmap: weekly incidence per week per federal state in 2020
fig, ax = pfunc.plot_heatmap(weekly_incidence_per_state,
                             title='case incidence per federal state over time',
                             filename='incidence_state',
                             annot=True, fmt='.1f')
# heatmap: weekly incidence per week per federal state in 2020 relative to overall incidence
fig, ax = pfunc.plot_heatmap_and_line(weekly_incidence_per_state,
                                      x_line=weekly_incidence.index,
                                      y_line=weekly_incidence, df_line=None,
                                      title1='case incidence (cases/100.000 people) per federal state over time relative to total case incidence in Germany',
                                      title2='total case incidence over time',
                                      filename='incidence_state_relative',
                                      annot=True, fmt='.1f')

fig, ax = pfunc.plot_line(clinical[['mean_age', 'no_symptoms_perc', 'hospital_perc', 'deaths_perc']],
                          title=f'asymptomatic cases vs. hospitalisaton and death rates \n(in relation to cases with respective information reported)',
                          filename='clinical_rates_reported')
fig, ax = pfunc.plot_line(clinical[['symptom_status_known', 'hospital_status_known']],
                          title=f'reporting rates of symptoms and hospitalisation status \ncompared to total number of known cases',
                          filename='reporting_rates')

#
# delay in reporting (date of infection vs. date of reporting to authorities): 0 if no delay or unknown, negative values due to reporting delays or errors (or maybe contact persons who fell sick later)?
fig = report_delay.hist(bins=61)
# report day of week
fig = overview['report_date_dayofweek'].hist(bins=7)


print('done')