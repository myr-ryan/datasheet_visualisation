from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import ColumnDataSource, Button, ColorPicker, HoverTool
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.glyphs import Scatter
from funcs import preprocess, plot_settings

import base64
import io
import pandas as pd
import numpy as np

# First create an empty plot
empty_data = {'x':[],
              'y':[]}
source = ColumnDataSource(data=empty_data)
source_backup = ColumnDataSource(data=empty_data)

# x_range=source.data["Paper ID"]
plot = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
plot.scatter('x', 'y', source=source)
# scatter = Scatter(x="Paper ID", y="y", marker="circle")
# plot.add_glyph(source, scatter)


# file_input = FileInput(accept='.xlsx', width=400)
file_input = FileInput(accept='.xlsx')


# Filters that you can apply on the plotting results, hard coded for now
filters = ['data_units', 'raw data availability', 'processed data availability', 'task', 'subspec', 'sample type']


# Set up widgets for variables that need to be plotted, and filters to apply
var_1 = Select(title="Please select var on x axis", value="(select)", options=[])
var_2 = Select(title="Please select var on y axis", value="(select)", options=[])


filter0_widget = Select(title=filters[0], value="All", options=[])

# Callback for file_input
def upload_data(attr, old, new):
    # Read excel file into dataframe
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')

    # Function 'preprocess' in file funcs.py
    # Returns the correct data types in each column and the possible selections of filters
    df, filter_values = preprocess(df)

    # Update selection widget: variables to plot
    numeric_var = list(df.select_dtypes(include='float64').columns.values)
    numeric_var.insert(0, "(select)")
    var_1.options = numeric_var
    var_2.options = numeric_var

    # Update selection widget: filters
    filter0_widget.options = filter_values[0]
    source.data = df
    source_backup.data = df
    print('Dataset uploaded successfully')

# Callback for button_apply
def update_plot():
    plot_var_1 = str(var_1.value)
    plot_var_2 = str(var_2.value)

    if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
        # text_warning = Text(x="x", y="y", text="Please select your variables to plot")
        # plot.title = "Please select your variables to plot!!"
        button_apply.label = "Please re-select!"
        button_apply.button_type = "danger"
        # text_warning = Text()
        # plot.add_layout(text_warning)
    
    else:
        button_apply.label = "Generate"
        button_apply.button_type = "primary"
        filter0 = str(filter0_widget.value)
        # plot.y_axis_label = var_value
        if filter0 == "All":
            selected = pd.DataFrame(source_backup.data)
        else:
            df = pd.DataFrame(source_backup.data)
            selected = df[df[filters[0]] == filter0]

        # Set x and y range, labels, function plot_settings in funcs.py
        plot_settings(plot, selected, plot_var_1, plot_var_2)

        selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
        source.data = selected
        

        # Create hover tool
        hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
        plot.add_tools(hover)




file_input.on_change('value', upload_data)




# Create a button widget for filters
button_apply = Button(label="Generate", button_type="primary")
button_apply.on_click(update_plot)

# # Create a color picker widget
# picker = ColorPicker(title = "Scatter Color")
# picker.js_link('color', scatter.glyph, 'line_color')



widgets = row(filter0_widget)
# widgets = row(plot_var)

curdoc().add_root(row(column(file_input, row(var_1, var_2), widgets, button_apply), plot))



    # data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]
# data_table = DataTable(source=source, columns=columns, width=400, height=400)