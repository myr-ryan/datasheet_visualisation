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

    plot = None
    if new == 'scatter':
        plot = ScatterPlot()
    else:
        print('Invalid plot type, please select again.')
    

    # For General_plot
    layout.children[0].children.insert(1, plot.upload_text)
    layout.children[0].children.insert(2, plot.upload_widget)
    layout.children[0].children.insert(4, plot.add_filter_button_widget)
    layout.children[0].children.insert(5, plot.filter_widgets)
    layout.children[0].children.insert(6, plot.add_range_button_widget)
    layout.children[0].children.insert(7, plot.range_selectors)
    layout.children[0].children.insert(8, plot.generate_button)

    # Plot specific
    layout.children[0].children.insert(3, plot.plot_spec_select_widgets)
    layout.children.insert(1, plot.plot_figure)
    
    plot.upload_widget.on_change('value', plot.cb_upload)
    plot.generate_button.on_click(functools.partial(plot.update_plot, button=plot.generate_button))



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






# range_sliders = column(column(row(general_plot.first_range_selector, general_plot.first_range_delete), general_plot.first_range_slider))

# curdoc().add_root(row(column(plot_type_select_widget, general_plot.upload_text, general_plot.upload_widget, plot_spec_select_widget, general_plot.filter_widgets, general_plot.add_filter_button_widget, range_sliders, general_plot.generate_button), plot))

layout = row(column(plot_type_select_widget))
curdoc().add_root(layout)