from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Button, ColorPicker
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.glyphs import Scatter
from funcs import preprocess

import base64
import io
import pandas as pd
import numpy as np

# First create an empty plot
empty_data = {'Paper ID':[],
              'y':[]}
source = ColumnDataSource(data=empty_data)
# x_range=source.data["Paper ID"]
plot = figure(height=400, width=500, title='Datasheet visualization')
plot.scatter('Paper ID', 'y', source=source)
# scatter = Scatter(x="Paper ID", y="y", marker="circle")
# plot.add_glyph(source, scatter)


# file_input = FileInput(accept='.xlsx', width=400)
file_input = FileInput(accept='.xlsx')

# All plotable variables from the file, hard coded
plotable = ['data_size_all', 'performance_auc', 'performance_precision (PPV)', 'performance_specificity', 
            'performance_NPV', 'performance_sensitivity (recall)', 'performance_F1', 'performance_accuracy']

# plotable.insert(0, 'All')

# Filters that you can apply on the plotting results, hard coded
filters = ['data_units', 'raw data availability', 'processed data availability', 'task', 'subspec', 'sample type']

# list to store all selectable values in the filters
filter_values = []
# filter0 = ['images', 'patients', 'cases', 'text']
# filter0.insert(0, 'All')



# Callback for file_input
def upload_data(attr, old, new):
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')
    df = preprocess(df, filter_values)
    source.data = df
    print('Dataset uploaded successfully')

# Callback for button_apply
def update_plot():
    var_value = str(plot_var.value)
    filter0 = str(filter0_widget.value)
    df = source.data  
    df = pd.DataFrame(df)
    selected = df[df[filters[0]] == filter0]
    x = selected["Paper ID"]
    y = selected[var_value]
    # source.data = dict(x=x, y=y)
    source.data = {"Paper ID": x, "y": y}
    # plot = figure(height=400, width=500, title='Datasheet visualization')
    # scatter = Scatter(x="Paper ID", y=var_value, marker="circle")
    # plot.add_glyph(source, scatter) 


file_input.on_change('value', upload_data)


# Set up widgets for variables that need to be plotted, and filters to apply
plot_var = Select(title="Variable to plot", value=plotable[0], options=plotable)
# filter0_widget = Select(title=filters[0], value="All", options=filter0)

# Create a button widget for filters
button_apply = Button(label="Apply", button_type="primary")
button_apply.on_click(update_plot)

# # Create a color picker widget
# picker = ColorPicker(title = "Scatter Color")
# picker.js_link('color', scatter.glyph, 'line_color')



# widgets = row(plot_var, filter0_widget)
widgets = row(plot_var)

curdoc().add_root(column(file_input, widgets, button_apply, plot))



    # data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]
# data_table = DataTable(source=source, columns=columns, width=400, height=400)