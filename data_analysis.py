import os
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func
from data_preprocess import data_load, data_clean

#### load, view and preprocess data ####
# for the sake of having a cleaner Notebook, I moved the loading and preoprocessing code to a script, data_preprocess.py.
# If you don't feel like checking out the details, this is what it does:
# load data from multiple csv files
# since some of the data was extracted from excel files with messy or incompatible formatting, cleaning included a lot of string extractions and replacements in different columns before numeric conversion could be done
# furthermore, I renamed some columns to be suitable for pandas (and for non-German speakers) and merged suitable tables together
# I made sure every table included a suitable time-based reference for comparison with the other tables

# load
overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, comorb =\
    data_load()
# preprocess
overview, casting, breakouts, cases_age, deaths, tests, comorb =\
    data_clean(overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, comorb)

#### data overview ####
total_cases = overview['AnzahlFall'].sum()
breakouts_time = breakouts.groupby('week')['num_breakouts'].sum()
breakouts_time_per_setting = breakouts.groupby(['week', 'sett_engl'])['num_breakouts'].sum()

print('done')