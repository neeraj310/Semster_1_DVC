import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from math import pi
import os
# ================================== 
#
#    Task1: Data Preprocessing
#
# ==================================


# T1.1: Read the .txt file into a dataframe using pandas (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
# hints on handling data reading error: 
# https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
# https://stackoverflow.com/questions/27896214/reading-tab-delimited-file-with-pandas-works-on-windows-but-not-on-mac
__file__ = 'ebd_US-AL-101_201801_201801_relMay-2018.txt'
my_absolute_dirpath = os.path.abspath(os.path.dirname(__file__))
df = pd.read_csv(...)

# df.head()

# T1.2: Data cleaning

# extracting data by attribute filtering
data_extracted1 = ...
print(data_extracted1.head(1))

# reset the index of data_extracted1 after filtering
data_reindexed = ...
print(data_reindexed.head(1))

# extracting data by multiple conditions
data_extracted2 = ...
print(data_extracted2.head(1))

# delete columns completely by using df.drop()
data_deleting = ...
print(data_deleting.head(1))


# ================================== 
#
#    Task2: Data Visualization
# 
# ==================================

# T2.1: Extract every first unique data item based on the scientific name and construct ColumnDataSource for scientific name and observation count
# reference: https://programminghistorian.org/en/lessons/visualizing-with-bokeh



# T2.2: Add the hovering tooltip



# T2.3: Visualize the data using bokeh plot functions



# T2.4: Save the plot using output_file





