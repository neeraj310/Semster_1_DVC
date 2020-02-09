import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file, save, curdoc
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.models.widgets import Select
from bokeh.layouts import column, row, gridplot
from datetime import datetime as dt
from math import pi, sqrt
import os


# ==================================================================

#        Task1: specify necessary drawing components 

# ==================================================================

# starting point: drawing a horizontal bar chart
# hint: https://bokeh.pydata.org/en/latest/docs/gallery/bar_intervals.html

__file__ = 'ebd_US-AL-101_201801_201801_relMay-2018.txt'
my_absolute_dirpath = os.path.abspath(os.path.dirname(__file__))



# read the dato into dataframe by using absolute path as specified in the lecture
df = pd.read_csv(my_absolute_dirpath+'/' + __file__, sep='\t')


# generate Y axix labels as a list of array (['2018-01-01', '2018-01-02', '2018-01-03',....]) by using only the "OBSERVATION DATE" column of data
# add two missing dates to make it complete, finally sort the labels

arr = df.rename(columns={"OBSERVATION DATE": "OBSERVATION_DATE"}).OBSERVATION_DATE.unique()
sorted_dates = np.sort(arr)
missing_dates = ['2018-01-06','2018-01-16']
ylabel = sorted(np.append(sorted_dates, missing_dates, axis=None ))





# ======== add control selector for selecting birds based on category ==========
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html
# how to add "all" category into the selector
# reference: https://stackoverflow.com//questions/50603077/bokeh-select-widget-does-not-update-plot

#p = figure(y_range=ylabel,width=1200,height=800)

category = []
category.append('All')
category.extend(df['CATEGORY'].unique().tolist())

#category = ...

# ===== optionally: =====
# category = []
# category.append('All')
# category.extend(df['CATEGORY'].unique().tolist())


# add the selector, options can be: category, name, locality, protocol, etc....
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html
select_category = Select(title="Option:", value="All", options=category)

#show(select_category)


# ==================================================================

#        Task2: define the datasource construction function 

# ==================================================================
# input: dataframe, either the original one or the updated one after triggering the selector
# output: column data source, which will be used for plotting, in our case, will serve as the input for the draw_plot function

# function to scale the "OBSERVATION COUNT" column
def scale_compute(x):
    return sqrt(x) * 2

def datasource_construct(df):

    # sort dfnew based on "OBSERVATION DATE", then reset the index for sorted dfnew
    df.sort_values(by=['OBSERVATION DATE']).reset_index(inplace=True)

    # scale the "OBSERVATION COUNT" column into reasonalbe number serving as the radius when later draw the circle
    # recommend to do the scaling for each item by computing "sqrt(item)*2"
    unscaled_list = df['OBSERVATION COUNT'].tolist()
    counts = []
    for item in unscaled_list:
        counts.append(scale_compute(item))
 


    # set the color corresponding to the observer number --> ====================
    observers = sorted(df['NUMBER OBSERVERS'].tolist()) # extract the column of "NUMBER OBSERVERS" and set it into a list

    colorset = ['lightseagreen', 'tomato', 'blueviolet', 'gold'] # can change to any other colors you like

    choices = {1: colorset[0], 2: colorset[1], 3: colorset[2], 13: colorset[3]} # 1,2,3,13 are the unique values of number observers

    colors = [choices.get(observers[i], "nothing") for i in range(0, len(observers))]


    # convert the TIME OBSERVATION into minutes for drawing the hbar
    df['TIME OBSERVATION'] = pd.to_timedelta(df['TIME OBSERVATIONS STARTED']) / pd.offsets.Minute(1)

    # add the observation ending minutes for drawing the hbar
    df['TIME OBSERVATIONS ENDED'] = df['TIME OBSERVATION'] + df['DURATION MINUTES']


    data = {'Year': list(df['OBSERVATION DATE']),
            'Starts': list(df['TIME OBSERVATION']),
            'Ends': list(df['TIME OBSERVATIONS ENDED']),# ending time of the observation
            'RealStarts': list(df['TIME OBSERVATIONS STARTED']), # list of column "TIME OBSERVATIONS STARTED", serving for hovertool
            'Duration': list(df['DURATION MINUTES']), # list of column "DURATION MINUTES", serving for hovertool
            'Counts': counts, # serves for the size of the circle
            'Name': list(df['COMMON NAME']),# list of "COMMON NAME", serving for hovertool
            'RealCounts': list(df['OBSERVATION COUNT']),# list of original "OBSERVATION COUNT", serving for hovertool
            'Observers': observers,
            'Colors': colors
            }


    source = ColumnDataSource(data=data)
    return source



# ==================================================================

#        Task3: define the update source function 

# ==================================================================
# input: fixed, but the actual input which will be used inside of the function is "value", which means the current selected value from the selector
# output: updated data source, serving as the input of the plot function too, whenever the selector is triggered
# how to add "all" category into the selector
# reference: https://stackoverflow.com/questions/50603077/bokeh-select-widget-does-not-update-plot


def update_source(attr, old, new):
    # create new dataframe after receiving the selected value when triggering the selector
    if select_category.value=="All":
        df_filter = df.copy()
    else:
        df_filter = df[df['CATEGORY']==select_category.value]
    
    # get new datasource by calling the datasource_construction function
    new_source = datasource_construct(df_filter)

    # update the source
    source.data.update(new_source.data)
    #p2.data_source.data = new_source.data
    return
    


# when the selector is triggered, the .on_change function will be called to run the corresponding update function
select_category.on_change('value', update_source)



# ===================================================================================================================

#        Task4: define the plot function which will be called initially and also whenever trigger the selector
# ===== plot the data based on time (one month data) and add other visual encodings for interesting information =====

# ===================================================================================================================
# input: columm datasource
# output: plot which should contain two main plots, hbar and circle, for the same data but different attributes
# add proper hover tool only on the circle plot by using "renderers" property in the HoverTool
# set up the x axis ticks into 24 hours scale, rend the hint below for more information

def draw_plot(source):
    #nsource = datasource_construct(df)
    p =  figure(x_range=(0,1440), y_range=ylabel, plot_width=900, plot_height=500) # add more properties for customization your graph
    #p.sizing_mode = 'scale_width'
    p1 = p.hbar(y='Year', right='Ends', left= 'Starts', fill_color ='Colors' , height=0.1, alpha=0.1, legend = 'Observers' , source=source)
    p2 = p.circle(x = 'Starts', y = 'Year', fill_color ='Colors', alpha=0.2, radius = 'Counts', source=source)


    # define the hovertool. and only make it effective for the circle plot p2 
    hover = HoverTool(renderers=[p2])
    hover.tooltips=[
        ("Observation Starts", "@RealStarts"),
        ("Duration in Minutes", "@Starts"),
        ("Observation Counts", "@RealCounts"),
        ("Bird's Name", "@Name"),
    ]

    # some more configuration of the plot, like labels, legend, etc.
    p.title.text ='Overview of birds observation record in one month'
    p.xaxis.formatter=NumeralTickFormatter(format="00:00:00")
    p.yaxis.major_label_orientation = pi/4
    p.xaxis.axis_label = 'Times in one day (24 hours)'
    p.legend.title = 'Observer Number'
    p.add_tools(hover)

	# Format x axis as hours and minutes as shown in the example solution: 
	# read "NumeralTickFormatter" in https://bokeh.pydata.org/en/latest/docs/user_guide/styling.html
	# https://bokeh.pydata.org/en/latest/docs/reference/models/formatters.html
    
    


    
    
    
    return p




# =============================================================================================

#        Task5: draw the figure and add bokeh server for interactive visualization

# =============================================================================================

# call datasource_construction function to get the source
source = datasource_construct(df)

# call draw_plot function to create the plots
p = draw_plot(source)
layout = column(p, row(select_category, width=300))

# ======= using bokeh server to run the application ========
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/server.html

curdoc().add_root(layout)


# ======= optional: output the result file ========
output_file('Final_result_abc.html')

#show(p)