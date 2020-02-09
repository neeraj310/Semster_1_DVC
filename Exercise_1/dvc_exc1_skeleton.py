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
filename = os.path.join(my_absolute_dirpath + '\ebd_US-AL-101_201801_201801_relMay-2018.txt')
df = pd.read_csv(filename, delimiter = '\t')
#df = pd.read_csv(r'E:\course_material\dvc_thursday\Exercise_1\ebd_US-AL-101_201801_201801_relMay-2018.txt', delimiter = '\t')
#print(df.head())

# T1.2: Data cleaning
# Remove spaces in the Column Names to perform parsing operations by Column Names
df.columns = df.columns.str.replace(' ', '_')
#print(df.head())

# extracting data by attribute filtering
# I am extracting all rows corresponding to the column values OBSERVATION_COUNT>2
# As I want the complete row(" All columns specific to a row"), I am giving column value as :
data_extracted1 = df.loc[df.OBSERVATION_COUNT>2, :]
print(data_extracted1.head(1))

# reset the index of data_extracted1 after filtering
# drop = 'True' to insert the new index as a column in the new dataframe
data_reindexed = data_extracted1.reset_index(drop = True, inplace=False)
print(data_reindexed.head(1))

# extracting data by multiple conditions
# I am extracting all rows which have OBSERVATION_COUNT>2 and SCIENTIFIC_NAME =='Setophaga coronata'
data_extracted2 = df.loc[(df.OBSERVATION_COUNT>2) & (df.SCIENTIFIC_NAME =='Setophaga coronata') , :]
print(data_extracted2.head(1))

# delete columns completely by using df.drop()
data_deleting = df.drop(['TAXONOMIC_ORDER','CATEGORY', 'COMMON_NAME'] , axis = 1)
print(data_deleting.head(1))




# ================================== 
#
#    Task2: Data Visualization
# 
# ==================================

# T2.1: Extract every first unique data item based on the scientific name and construct ColumnDataSource for scientific name and observation count
# reference: https://programminghistorian.org/en/lessons/visualizing-with-bokeh

# Extract every first unique data item based on the scientific name
df2 = df.drop_duplicates(subset = 'SCIENTIFIC_NAME', keep = 'first')

# Create a new data frame with 2 columns 'SCIENTIFIC_NAME', 'OBSERVATION_COUNT'
df3 = df2[['SCIENTIFIC_NAME', 'OBSERVATION_COUNT']]
df3.reset_index(drop = True, inplace=True)

# Construct ColumnDataSource for scientific name and observation count
source = ColumnDataSource(df3)

# Create the x labels Name List
sname = source.data['SCIENTIFIC_NAME'].tolist()

# Specify the dimensions of the figure
p = figure(plot_width=1500, plot_height=800, x_range = sname)

# T2.3: Visualize the data using bokeh plot functions
p.vbar(x = 'SCIENTIFIC_NAME', top = 'OBSERVATION_COUNT',source=source, width=0.7) 

# Add title and specify X and Y labels
p.title.text ='Birds Observation number based on their scientifc names'
p.xaxis.axis_label = 'Scientific Name'
p.yaxis.axis_label = 'Observation Number'

p.y_range.start = 0
p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = "vertical"
p.outline_line_color = None

# T2.2: Add the hovering tooltip
hover = HoverTool()
hover.tooltips = [('Observation count','@OBSERVATION_COUNT')]

hover.mode = 'vline'
p.add_tools(hover)

# T2.4: Save the plot using output_file   
# Create the output html file
output_file('columndatasource_example_2.html')

show(p)













