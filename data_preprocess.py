import pandas as pd
import math
import functools as func

def data_load():

    #### general covid case overview (RKI dashboard data)
    overview = pd.read_csv("data/RKI/RKI_COVID19.csv")

    #### reproductive factor calculation from RKI nowcasting
    casting = pd.read_csv("data/RKI/Nowcasting_Zahlen_csv.csv", sep=';')

    #### cases which were be counted as a breakout
    breakouts = pd.read_csv("data/RKI/Ausbruchsdaten.csv", sep=';')

    #### cases per age
    cases_age1 = pd.read_csv("data/RKI/Altersverteilung_total.csv", sep=';')
    cases_age2 = pd.read_csv("data/RKI/Altersverteilung_incidence.csv", sep=';')

    #### deaths
    deaths1 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_all.csv", sep=';')
    deaths2 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_age.csv", sep=';')
    deaths3 = pd.read_csv("data/RKI/COVID-19_Todesfaelle_gender.csv", sep=';')

    #### PRC test capacities
    tests1 = pd.read_csv("data/RKI/Testzahlen-gesamt.csv", sep=';')
    tests2 = pd.read_csv("data/RKI/Testzahlen-rueck.csv", sep=';')

    #### comorbidities
    comorb = pd.read_csv("data/RKI/Klinische_Aspekte.csv", sep=';', skiprows=2)

    return overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, comorb


def data_clean(overview, casting, breakouts, cases_age1, cases_age2, deaths1, deaths2, deaths3, tests1, tests2, clinical):
    #### general covid case overview (RKI dashboard data)

    # rename report and reference date (date of suspected/confirmed infection), calculate delay
    overview['report_date'] = pd.to_datetime(overview['Meldedatum'], format='%Y/%m/%d %H:%M:%S').dt.date
    overview['ref_date'] = pd.to_datetime(overview['Refdatum'], format='%Y/%m/%d %H:%M:%S').dt.date
    overview['report_delay'] = (overview['report_date'] - overview['ref_date']).dt.days
    overview.rename(columns={'IstErkrankungsbeginn': 'ref_eq_rep'})
    # create new date columns for weeks and days to compare with other tables
    overview['ref_date_dayofweek'] = pd.DatetimeIndex(overview['ref_date']).dayofweek
    overview['ref_date_year'] = pd.DatetimeIndex(overview['ref_date']).year
    overview['ref_date_week'] = pd.DatetimeIndex(overview['ref_date']).weekofyear
    # map week 53 to 2020
    overview.loc[((overview['ref_date_year'] == 2021) & (overview['ref_date_week'] == 53)), 'ref_date_year'] = 2020
    overview['report_date_dayofweek'] = pd.DatetimeIndex(overview['report_date']).dayofweek
    overview['report_date_year'] = pd.DatetimeIndex(overview['report_date']).year
    overview['report_date_week'] = pd.DatetimeIndex(overview['report_date']).weekofyear
    # map week 53 to 2020
    overview.loc[((overview['report_date_year'] == 2021) & (overview['report_date_week'] == 53)), 'report_date_year'] = 2020

    # drop inconclusive/redundant columns
    overview.drop(['Altersgruppe2', 'Datenstand', 'Meldedatum', 'Refdatum', 'ObjectId'], axis=1, inplace=True)

    #### reproductive factor calculation from RKI nowcasting

    # drop faulty rows and rename columns
    casting = casting \
        .drop(casting.index[319::], axis=0) \
        .rename(columns={'Datum': 'date',
                         'Schätzer_Neuerkrankungen': 'est_new_cases',
                         'UG_PI_Neuerkrankungen': 'pred_lower',
                         'OG_PI_Neuerkrankungen': 'pred_upper',
                         'Schätzer_Neuerkrankungen_ma4': 'est_new_cases_smooth',
                         'UG_PI_Neuerkrankungen_ma4': 'pred_lower_smooth',
                         'OG_PI_Neuerkrankungen_ma4': 'pred_upper_smooth',
                         'Schätzer_Reproduktionszahl_R': 'est_r',
                         'UG_PI_Reproduktionszahl_R': 'r_lower',
                         'OG_PI_Reproduktionszahl_R': 'r_upper',
                         'Schätzer_7_Tage_R_Wert': 'est_r7',
                         'UG_PI_7_Tage_R_Wert': 'r7_upper',
                         'OG_PI_7_Tage_R_Wert': 'r7_lower'})
    # add date and week
    casting['date'] = pd.to_datetime(casting['date'], format='%d.%m.%Y').dt.date
    casting['week'] = pd.DatetimeIndex(casting['date']).weekofyear
    # remove incompatible string characters, columns to floats
    for col in ['est_r', 'r_upper', 'r_lower', 'est_r7', 'r7_upper', 'r7_lower']:
        casting[col] = casting[col].apply(lambda x: math.nan if x == '.' else float(x.replace(',', '.')))

    #### cases which were be counted as a breakout

    # drop redundant columns, rename columns
    breakouts = breakouts \
        .rename(columns={'Meldewoche': 'week', 'n': 'num_breakouts'}) \
        .drop('sett_f', axis=1)

    #### cases per age

    # remove incompatible string characters, columns to floats
    for col in cases_age2.columns[1::]:
        cases_age2[col] = cases_age2[col].str.replace(',', '.').astype('float')
    # merge
    cases_age = pd.merge(cases_age1, cases_age2, on='Altersgruppe', suffixes=('_total', '_incidence'))

    #### deaths

    # drop redundant columns, rename columns
    deaths1 = deaths1 \
        .rename(columns={'Sterbewoche': 'week', 'Anzahl verstorbene COVID-19 Fälle': 'deaths_total'}) \
        .drop('Sterbejahr', axis=1)
    deaths2 = deaths2 \
        .rename(columns={'Sterbewoche': 'week',
                         'AG 0-9 Jahre': 'age_0',
                         'AG 10-19 Jahre': 'age_10',
                         'AG 20-29 Jahre': 'age_20',
                         'AG 30-39 Jahre': 'age_30',
                         'AG 40-49 Jahre': 'age_40',
                         'AG 50-59 Jahre': 'age_50',
                         'AG 60-69 Jahre': 'age_60',
                         'AG 70-79 Jahre': 'age_70',
                         'AG 80-89 Jahre': 'age_80',
                         'AG 90+ Jahre': 'age_90'}) \
        .drop('Sterbjahr', axis=1)
    deaths3 = deaths3 \
        .rename(columns={'Sterbewoche': 'week',
                         'Männer, AG 0-19 Jahre': 'M0_19',
                         'Männer, AG 20-39 Jahre': 'M20_39',
                         'Männer, AG 40-59 Jahre': 'M40_59',
                         'Männer, AG 60-79 Jahre': 'M60_79',
                         'Männer, AG 80+ Jahre': 'M80',
                         'Frauen, AG 0-19 Jahre': 'F0_19',
                         'Frauen, AG 20-39 Jahre': 'F20_39',
                         'Frauen, AG 40-59 Jahre': 'F40_59',
                         'Frauen, AG 60-79 Jahre': 'F60_79',
                         'Frauen, AG 80+ Jahre': 'F80'}) \
        .drop('Sterbjahr', axis=1)
    # merge
    deaths = func.reduce(lambda left, right: pd.merge(left, right, on='week'), [deaths1, deaths2, deaths3])
    # assume '<4' deaths as 3
    deaths = deaths.replace('<4', '3').astype('int')

    #### PRC test capacities

    # rename columns
    tests1 = tests1.rename(columns={'KW, für die die Angabe prognostisch erfolgt ist:': 'week',
                                    'Anzahl übermittelnde Labore': 'laboratories',
                                    'Testkapazität pro Tag': 'daily_cap',
                                    'Theoretische wöchentliche Kapazität anhand von Wochenarbeitstagen': 'weekly_cap_est',
                                    'Reale Testkapazität zum Zeitpunkt der Abfrage': 'weekly_cap_real'})
    # remove incompatible string characters and get week, test capacities as integers
    tests1['week'] = tests1['week'].str.split('KW').str[1].astype('int')
    tests1['weekly_cap_est'] = tests1['weekly_cap_est'].replace('-', 0).astype('int')
    tests1['weekly_cap_real'] = tests1['weekly_cap_real'].replace('-', 0).astype('int')
    # drop faulty columns and rename
    tests2 = tests2.drop(['Unnamed: 3'], axis=1) \
        .rename(columns={'Labore mit Rückstau': 'laboratories_tailback',
                         'KW': 'week',
                         'Probenrückstau': 'tests_tailback'})
    # merge
    tests = pd.merge(tests1, tests2, on='week', how='outer').fillna(0)
    # alias weeks for 2021 with higher numbers
    tests['week'].iloc[43] = 54
    tests['week'].iloc[44] = 55

    #### clinical data

    # remove incompatible string characters and columns as integers
    clinical = clinical.rename(columns={'Meldejahr': 'year',
                                    'MW': 'week',
                                    'Fälle gesamt': 'cases_tot',
                                    'Mittelwert Alter (Jahre)': 'mean_age',
                                    'Männer': 'male_perc',
                                    'Frauen': 'female_perc',
                                    'Anzahl mit Angaben zu Symptomen': 'symptoms_reported',
                                    'Anteil keine, bzw. keine für COVID-19 bedeutsamen Symptome': 'no_symptoms_perc',
                                    'Anzahl mit Angaben zur Hospitalisierung': 'hospital_reported',
                                    'Anzahl hospitalisiert': 'hospital_num',
                                    'Anteil hospitalisiert': 'hospital_perc',
                                        'Anzahl Verstorben': 'deaths_num',
                                        'Anteil Verstorben': 'deaths_perc'
                                        }).drop(['Unnamed: 0'], axis=1)
    # remove incompatible string characters, columns to floats
    for col in ['male_perc', 'female_perc', 'no_symptoms_perc', 'hospital_perc', 'deaths_perc']:
        clinical[col] = clinical[col].str.replace(',', '.').astype('float')

    return overview, casting, breakouts, cases_age, deaths, tests, clinical












