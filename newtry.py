from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import ColumnDataSource, Button, ColorPicker, HoverTool, DateRangeSlider, MultiChoice, CheckboxGroup, Div
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.glyphs import Scatter
from funcs import preprocess, plot_settings, code_2_text, text_2_code

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
# filters = ['data_units', 'raw data availability', 'processed data availability', 'task', 'subspec', 'sample type']


# Set up widgets for variables that need to be plotted, and filters to apply
var_1 = Select(title="Please select var on x axis", value="(select)", options=[])
var_2 = Select(title="Please select var on y axis", value="(select)", options=[])


# filter_widget = Select(, value="None", options=[])
task_text = Div(text='''Select task:''')
task_widget = CheckboxGroup(name='Tasks', labels=[], active=[])
subspec_text = Div(text='''Select subspecies:''')
subspec_widget = CheckboxGroup(name='Subspec', labels=[], active=[])
filter_text = Div(text='''Select other filters:''')
filter_widget = CheckboxGroup(name='Filters', labels=[], active=[])

# Callback for file_input
def upload_data(attr, old, new):
    # Read excel file into dataframe
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')

    # Function 'preprocess' in file funcs.py
    # Returns the correct data types in each column and the possible selections of filters
    df, task_filters, subspec_filters, other_filters = preprocess(df)

    # Update selection widget: variables to plot
    numeric_var = list(df.select_dtypes(include='float64').columns.values)
    numeric_var.insert(0, "(select)")
    var_1.options = numeric_var
    var_2.options = numeric_var

    # Update selection widget: filters
    # print(filter_values)
    task_widget.labels = task_filters
    subspec_widget.labels = subspec_filters
    filter_widget.labels = other_filters
    source.data = df
    source_backup.data = df
    print('Dataset uploaded successfully')

# Callback for button_apply
def update_plot():
    plot_var_1 = str(var_1.value)
    plot_var_2 = str(var_2.value)

    if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
        button_apply.label = "Please re-select variables!"
        button_apply.button_type = "danger"  
    else:
        button_apply.label = "Generate"
        button_apply.button_type = "primary"

        task_list = task_widget.active
        subspec_list = subspec_widget.active  
        filter_list = filter_widget.active

        selected = pd.DataFrame(source_backup.data)

        if task_list:
            task_names = [task_widget.labels[t] for t in task_list]
            selected = selected[selected[task_names].any(axis='columns')]

        if subspec_list:
            subspec_names = [subspec_widget.labels[s] for s in subspec_list]
            selected = selected[selected[subspec_names].any(axis='columns')]


        for f in filter_list:        
            column_name = filter_widget.labels[f]             
        
            # Check if the filter is categorical data
            is_category = (selected[column_name].dtype == 'category')

            if is_category:
                f_value = []
                for value_widget in widgets.children[1].children:
                    if value_widget.title == column_name:
                        f_value = value_widget.value
                        f_value = [text_2_code(column_name, x) for x in f_value]
                
                if f_value:
                    selected = selected[selected[column_name].isin(f_value)]

            else:
                df = pd.DataFrame(source_backup.data)
                selected = selected[df[column_name] == True]      


        # Set x and y range, labels, function plot_settings in funcs.py
        plot_settings(plot, selected, plot_var_1, plot_var_2)

        selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
        source.data = selected
        

        # Create hover tool
        hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
        plot.add_tools(hover)


# Inputs:
#       attr
#       old: includes all values in argument 'active' in 'filter_widget' CheckBox before checking, values are indices of selected filters, e.g. [0, 1]
#       new: includes all values in argument 'active' in 'filter_widget' CheckBox after checking, values are indices of selected filters, e.g. [0, 1, 2]
def update_filter(attr, old, new):
    # if add a filter
    if len(new) > len(old):
        # Find the newly selected filter
        old_temp = set(old)
        selected_column_index = [x for x in new if x not in old_temp][0]
        column_name = filter_widget.labels[selected_column_index]  
        
        # Check if the filter is categorical data
        is_category = (source.data[column_name].dtype == 'category')
        # print(column_name + ': ' +  str(is_category)) 

        if is_category:
            df = pd.DataFrame(source_backup.data)
            options = df[column_name]
            options = list(map(str, list(set(options.tolist()))))
            options = [code_2_text(column_name, x) for x in options]

            selectable_values = MultiChoice(title=column_name, value=[], options=options)
            widgets.children[1].children.insert(0, selectable_values)
                
               
    # if unselect/remove a filter
    else:
        # Find the unselected/removed filter
        new_temp = set(new)
        deleted_column_index = [x for x in old if x not in new_temp][0]
        column_name = filter_widget.labels[deleted_column_index] 
        # Check if the filter is categorical data
        is_category = (source.data[column_name].dtype == 'category')
        # print(column_name + ': ' +  str(is_category)) 

        if is_category:
            # Delete the unselected/removed filter widget
            for value_widget in widgets.children[1].children:
                if value_widget.title == column_name:
                    widgets.children[1].children.remove(value_widget)


file_input.on_change('value', upload_data)
filter_widget.on_change('active', update_filter)




# Create a button widget for filters
button_apply = Button(label="Generate", button_type="primary")
button_apply.on_click(update_plot)

# # Create a color picker widget
# picker = ColorPicker(title = "Scatter Color")
# picker.js_link('color', scatter.glyph, 'line_color')


widgets = row(filter_widget, column())
# widgets = row(plot_var)

curdoc().add_root(column(file_input, row(var_1, var_2), row(task_text, task_widget, subspec_text, subspec_widget, filter_text, widgets), button_apply, plot))



# data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]
# data_table = DataTable(source=source, columns=columns, width=400, height=400)