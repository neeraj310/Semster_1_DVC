import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file, save, curdoc
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.models.widgets import Select
from bokeh.layouts import column, row, gridplot
from datetime import datetime as dt
from math import pi, sqrt


# ==================================================================

#        Task1: specify necessary drawing components 

# ==================================================================

# starting point: drawing a horizontal bar chart
# hint: https://bokeh.pydata.org/en/latest/docs/gallery/bar_intervals.html




# read the dato into dataframe by using absolute path as specified in the lecture
df = ...


# generate Y axix labels as a list of array (['2018-01-01', '2018-01-02', '2018-01-03',....]) by using only the "OBSERVATION DATE" column of data
# add two missing dates to make it complete, finally sort the labels
ylabel = ...




# ======== add control selector for selecting birds based on category ==========
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html
# how to add "all" category into the selector
# reference: https://stackoverflow.com//questions/50603077/bokeh-select-widget-does-not-update-plot


category = ...

# ===== optionally: =====
# category = []
# category.append('All')
# category.extend(df['CATEGORY'].unique().tolist())


# add the selector, options can be: category, name, locality, protocol, etc....
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html
select_category = Select(...)




# ==================================================================

#        Task2: define the datasource construction function 

# ==================================================================
# input: dataframe, either the original one or the updated one after triggering the selector
# output: column data source, which will be used for plotting, in our case, will serve as the input for the draw_plot function

def datasource_construct(dfnew):

    # sort dfnew based on "OBSERVATION DATE", then reset the index for sorted dfnew


    # scale the "OBSERVATION COUNT" column into reasonalbe number serving as the radius when later draw the circle
    # recommend to do the scaling for each item by computing "sqrt(item)*2"
    counts = ...


    # set the color corresponding to the observer number --> ====================
    observers = ... # extract the column of "NUMBER OBSERVERS" and set it into a list

    colorset = ['lightseagreen', 'tomato', 'blueviolet', 'gold'] # can change to any other colors you like

    choices = {1: colorset[0], 2: colorset[1], 3: colorset[2], 13: colorset[3]} # 1,2,3,13 are the unique values of number observers

    colors = [choices.get(observers[i], "nothing") for i in ...]


    # convert the TIME OBSERVATION into minutes for drawing the hbar
    df['TIME OBSERVATION'] = pd.to_timedelta(df['TIME OBSERVATIONS STARTED']) / pd.offsets.Minute(1)

    # add the observation ending minutes for drawing the hbar
    df['TIME OBSERVATIONS ENDED'] = df['TIME OBSERVATION'] + df['DURATION MINUTES']


    data = {'Year': list(df['OBSERVATION DATE']),
            'Starts': list(df['TIME OBSERVATION']),
            'Ends': # ending time of the observation
            'RealStarts': # list of column "TIME OBSERVATIONS STARTED", serving for hovertool
            'Duration': # list of column "DURATION MINUTES", serving for hovertool
            'Counts': counts, # serves for the size of the circle
            'Name': # list of "COMMON NAME", serving for hovertool
            'RealCounts': # list of original "OBSERVATION COUNT", serving for hovertool
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

    
    # get new datasource by calling the datasource_construction function
    

    # update the source
    


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
    p =  figure(x_range=(0,1440), y_range=ylabel) # add more properties for customization your graph
    p1 = p.hbar(.....)
    p2 = p.circle(...)

    # some more configuration of the plot, like labels, legend, etc.




	# Format x axis as hours and minutes as shown in the example solution: 
	# read "NumeralTickFormatter" in https://bokeh.pydata.org/en/latest/docs/user_guide/styling.html
	# https://bokeh.pydata.org/en/latest/docs/reference/models/formatters.html
    



    # define the hovertool. and only make it effective for the circle plot p2 
    
    
    return p




# =============================================================================================

#        Task5: draw the figure and add bokeh server for interactive visualization

# =============================================================================================

# call datasource_construction function to get the source
source = ... 

# call draw_plot function to create the plots
p = ... 


# ======= using bokeh server to run the application ========
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/server.html



# ======= optional: output the result file ========



