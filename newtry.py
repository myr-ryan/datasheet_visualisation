from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Button, ColorPicker, HoverTool, RangeSlider, MultiChoice, CheckboxGroup, Div, MultiSelect
from bokeh.models.widgets import Slider, TextInput, Select, FileInput
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.glyphs import Scatter

from Plot_Data import *
from Scatter_plot import *
from General_plot import *
import functools
import base64
import io
import pandas as pd
import numpy as np


def plot_type_creation(attr, old, new):

    plot_spec_select_widget = row()

    plot = None
    if new == 'scatter':
        plot = ScatterPlot()
    else:
        print('Invalid plot type, please select again.')
    
    # plot_spec_select_widget.children += plot.plot_spec_select_widgets
    # plot.plot_spec_select_widget = plot_spec_select_widget

    # For General_plot
    layout.children[0].children.insert(1, plot.upload_text)
    layout.children[0].children.insert(2, plot.upload_widget)
    layout.children[0].children.insert(4, plot.filter_widgets)
    layout.children[0].children.insert(5, plot.add_filter_button_widget)
    # layout.children[0].children.insert(6, plot.range_selector)
    layout.children[0].children.insert(6, plot.generate_button)

    # Plot specific
    layout.children[0].children.insert(3, plot_spec_select_widget)
    layout.children.insert(1, plot.plot_figure)
    
    plot.upload_widget.on_change('value', plot.upload_data)
    plot.generate_button.on_click(functools.partial(plot.update_plot, button=plot.generate_button))


def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2


# # First create an empty plot
# empty_data = {'x':[],
#               'y':[]}

# scatter_plot_data = Plot_Data(empty_data)
# plot = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
# plot.scatter('x', 'y', source=scatter_plot_data.source)


plot_type_select_widget = Select(title="Please select a plot type", value="(select)", options=['(select)', 'scatter'], width=245, height=50, margin=(0,0,50,0))


# general_plot = GeneralPlot(scatter_plot_data, plot_spec_select_widget)
plot_type_select_widget.on_change('value', plot_type_creation)



# def convert_bool(value_list):
#     res = []
#     for x in value_list:
#         if (x == '0') or (x == '0.0'):
#             res.append(False)
#         elif (x == '1') or (x == '1.0'):
#             res.append(True)

#     return res if res != [] else value_list




def update_slider(attr, old, new, slider):
    df = pd.DataFrame(scatter_plot_data.source_backup.data)
    min_value = df[new].min()
    max_value = df[new].max()
    slider.start = min_value
    slider.end = max_value
    slider.value = (min_value, max_value)
    slider.step = (max_value - min_value) // 100
    slider.title = str(new)


# range_sliders = column(column(row(general_plot.first_range_selector, general_plot.first_range_delete), general_plot.first_range_slider))

# curdoc().add_root(row(column(plot_type_select_widget, general_plot.upload_text, general_plot.upload_widget, plot_spec_select_widget, general_plot.filter_widgets, general_plot.add_filter_button_widget, range_sliders, general_plot.generate_button), plot))

layout = row(column(plot_type_select_widget))
curdoc().add_root(layout)