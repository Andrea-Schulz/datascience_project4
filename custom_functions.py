import os
import csv
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import functools as func

def remove_column_substr(df, substr):
    df.columns = df.columns.str.replace(substr, '')
    return df