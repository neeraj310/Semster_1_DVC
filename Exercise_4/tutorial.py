"""
Tutorial
Bokeh Server Callbacks


run with
bokeh serve --show tutorial.py
"""

import numpy as np
from random import sample, choices
import datetime
import pandas as pd

from bokeh.plotting import figure, show, output_file, curdoc
from bokeh.layouts import layout, column, row
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource, Slider, Range1d, LinearAxis, CheckboxButtonGroup, \
    Div, Rect, Circle, Quad, Button, AnnularWedge
from bokeh.transform import linear_cmap
from bokeh.palettes import magma, plasma
from bokeh.colors import RGB

from pyproj import transform, Proj, Transformer

"""
=============
Pandas Basics
=============
"""

"""
=======================
DataSources
=======================
ColumnDataSources can be created from a dictionary or a pandas.DataFrame

1. Create two DataSources and two plots containing the same data, 

"""
df = pd.DataFrame()
df['xs'] = np.arange(0, 10)
df['ys'] = np.random.rand(10)

# Create a ColumnDataSource directly from a pandas dataframe
ds = ColumnDataSource(df)

# Create a ColumnDataSource from a python dict
d1 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10)
))


"""
=======================
Callback: Changing Data
=======================

This example shows how to update the datasource within a bokeh callback. 
Here, a button click will generate new random data. 
"""

d1 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10)
))

p1 = figure(plot_width=400, plot_height=400)
p1.line(x = "xs", y="ys", line_width=2, source=d1)


def callback_change_data():
    # Generate some new data
    new_data = ColumnDataSource(dict(
        xs = np.arange(0, 10),
        ys = np.random.rand(10)
    ))

    # Always exchange the complete datasource!
    d1.data = new_data.data


btn_change = Button(name="Change Data")
btn_change.on_click(callback_change_data)



"""
=========================================
Callback: Multiple Glyphs Hide/Show Glyphs
=========================================

figure().<your-glyph>() returns a renderer, if this is stored, one can later change its visibility.

"""

d2 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10)
))
p2 = figure(plot_width=400, plot_height=400)
renderer = dict()

renderer['circles'] = p2.circle(x = "xs", y="ys", color="red", size=10, line_width=2, source=d2)
renderer['lines'] = p2.line(x = "xs", y="ys", line_width=2, source=d2)


def callback_glyphs(new):
    print("Active Checkboxes:", new)
    renderer['circles'].visible = False
    renderer['lines'].visible = False

    if 0 in new:
        renderer['circles'].visible = True
    if 1 in new:
        renderer['lines'].visible = True


btn_glyphs = CheckboxButtonGroup(labels=["Circles", "Lines"], active=[0, 1])
btn_glyphs.on_click(callback_glyphs)


"""
=======================
Two Axes
=======================

"""

d_axis_1 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10)
))

d_axis_2 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10) * 100
))

p_axis = figure(plot_width=400, plot_height=400, y_range = (0.0,1.0))
p_axis.line(x = "xs", y="ys", line_width=2, source=d_axis_1)

p_axis.extra_y_ranges = {"AnotherAxis": Range1d(start=0, end=100, bounds=(0.0, 100))}
p_axis.add_layout(LinearAxis(y_range_name='AnotherAxis', axis_label='AnotherAxis range between 0 and 100'), 'right')
p_axis.circle(x = "xs", y="ys", line_width=2, size=15, line_color="red", y_range_name="AnotherAxis", source=d_axis_2)

# Changing the color of the second label
p_axis.yaxis[1].major_label_text_color = "red"


"""
===================
Callback: Selection
===================

A selection callback in bokeh usually returns the indices of the data points currently 
selected in the ColumnDataSource. 

"""

d3 = ColumnDataSource(dict(
    xs = np.arange(0, 10),
    ys = np.random.rand(10)
))

# Add a Lasso-Selection tool
p3 = figure(plot_width=400, plot_height=400, tools=['lasso_select'])
circle_renderer = p3.circle(x = "xs", y="ys", size=10, source=d3)

# Customize the glyphs for selection and non-selection
circle_renderer.nonselection_glyph = Circle(fill_color="#3c6f9c", fill_alpha=0.5)
circle_renderer.selection_glyph = Circle(fill_color="red", fill_alpha=1.0)

# p4 shares the ColumnDataSource with p3, the selection is therefore always in sync
p4 = figure(plot_width=400, plot_height=400)
p4.vbar(bottom=0, top="ys", width=0.9, x="xs", source=d3)


# Creating a new Plot to indicate the percentage of selected items
# This needs a new datasource which we synchronize in the callback_selection with d3
d4 = ColumnDataSource(dict(xs=[0],
                           ys=[0],
                           value=[0.0],
                           text=["0%"]))
p5 = figure(plot_width=400, plot_height=400)
p5.annular_wedge(x="xs", y="ys",  start_angle=0.0, end_angle="value", inner_radius = 0.3, outer_radius=0.8, source=d4)
p5.text(x=0, y=0, text="text", source=d4)


def callback_selection(attr, old, new):
    print("Selected Indices:", new)

    # we want to change the size of the circle in p4 based on the number
    # of selected in p3
    new_value = len(new) / len(d3.data['xs'])
    radians =  new_value * 2 * np.pi
    d4.data = ColumnDataSource(dict(xs=[0],
                                    ys=[0],
                                    value=[radians],
                                    text=[str(new_value * 100) + "%"])).data


# Hook the callback to the on_change event
d3.selected.on_change("indices", callback_selection)




"""
=================
WorldMap Examples
=================
"""


def coord2mercator(long, lat, varb = False):
    """
    Projects a decimal coordinate onto a web mercator plane.
    Can also be given as numpy.ndarray

    :param long: A single or array of decimal longitude values
    :param lat: A single or array of decimal latitude values
    :return: an array of tuples, each (Long, Lat) in web mercator
    """
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    return transformer.transform(lat, long)


tile_provider = get_provider(Vendors.CARTODBPOSITRON)

xmin, ymin = coord2mercator(-179.999, -80.999)
xmax, ymax = coord2mercator(179.999, 80.999)

# range bounds supplied in web mercator coordinates
world_map_left = figure(x_range=(xmin, xmax), y_range=(ymin, ymax),
                        x_axis_type="mercator", y_axis_type="mercator",
                        output_backend="webgl",
                        tools=["tap", "lasso_select", "wheel_zoom", "pan"],
                        width=800, height=800)

# Add the countries
world_map_left.add_tile(tile_provider)

world_map_left.xaxis.axis_label = "Longitude"
world_map_left.yaxis.axis_label = "Latitude"


"""
Projecting points into the web mercator coordinate system
"""

# Project the decimal coordinates into WebMercator
decimal_coords_zurich = [47.36667, 8.55]    # [Latitude, Longitude]
decimal_coords_accra =  [5.55602, -0.1969]  # [Latitude, Longitude]
decimal_coords = np.array([decimal_coords_zurich, decimal_coords_accra])

mercatorLong, mercatorLat = coord2mercator(decimal_coords[:,1], decimal_coords[:, 0])

d_world_map = ColumnDataSource(dict(
    mercatorLong=mercatorLong,
    mercatorLat = mercatorLat,
    location_name = ["Zurich", "Accra"]
))

world_map_left.circle_cross(x="mercatorLong", y ="mercatorLat", size=5, fill_color="#fc0324", source=d_world_map)
world_map_left.text(x="mercatorLong", y ="mercatorLat", text="location_name", source=d_world_map)


"""
WorldMap, with linked axes, and area
"""

# range bounds supplied in web mercator coordinates
world_map_right = figure(x_range=world_map_left.x_range, y_range=world_map_left.y_range,
                        x_axis_type="mercator", y_axis_type="mercator",
                        output_backend="webgl",
                        tools=["tap", "lasso_select", "wheel_zoom", "pan"],
                        width=800, height=800)

# Add the countries
world_map_right.add_tile(tile_provider)

N_BINS_LAT = 18
N_BINS_LONG = 36

# xs1 and ys1 is the left lower corner, xs2, ys2 is the right upper corner
xs1, ys1, xs2, ys2, value = [], [], [], [], []

for x in range(N_BINS_LONG):
    for y in range(N_BINS_LAT):
        # Make sure to clip the ranges to not get inf values
        xs1.append(np.clip(x * (360 / N_BINS_LONG) - 180, -179.99, 179.99))
        ys1.append(np.clip(y * (180 / N_BINS_LAT) - 90, -89.99, 89.99))
        xs2.append(np.clip((x + 1) * (360 / N_BINS_LONG) - 180, -179.99, 179.99))
        ys2.append(np.clip((y + 1) * (180 / N_BINS_LAT) - 90, -89.99, 89.99))
        value.append(np.random.rand()/1.0 * 0.2)

# Projecting them into web mercator coordinates
xs1, ys1 = coord2mercator(xs1, ys1)
xs2, ys2 = coord2mercator(xs2, ys2)

d_grid = ColumnDataSource(dict(
    xs1 = xs1,
    ys1 = ys1,
    xs2 = xs2,
    ys2 = ys2,
    value=value
))

world_map_right.quad(left="xs1",
                    top="ys1",
                    right="xs2",
                    bottom="ys2",
                    fill_alpha="value",
                    line_alpha=1.0,
                    source=d_grid)

lt = column([
        Div(text="""<h1> Visualization Interactions in Bokeh </h1>"""),
        Div(text="""<h1> Changing Data</h1>"""),
        btn_change,
        p1,

        Div(text="""<h1> Show/Hide Glyphs</h1>"""),
        btn_glyphs,
        p2,

        Div(text="""<h1> Multiple Axis</h1>"""),
        p_axis,

        Div(text="""<h1> Selection</h1>"""),
        row([p3, p4, p5], sizing_mode="stretch_width"),


        Div(text="""<h1> World Map</h1>"""),
        row([world_map_left, world_map_right], sizing_mode="stretch_width")
    ], sizing_mode="stretch_width")

curdoc().add_root(lt)