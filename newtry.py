from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import ColumnDataSource, Button, ColorPicker, HoverTool, DateRangeSlider, MultiChoice, CheckboxGroup, Div, MultiSelect
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.glyphs import Scatter

from Plot_Data import *
import functools
import base64
import io
import pandas as pd
import numpy as np

# First create an empty plot
empty_data = {'x':[],
              'y':[]}

scatter_plot_data = Plot_Data(empty_data)
plot = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
plot.scatter('x', 'y', source=scatter_plot_data.source)

upload_prompt = Div(text='''Please upload your datasheet''')
file_input = FileInput(accept='.xlsx', width=500, height=40, margin=(0,0,25,0))

# Set up widgets for variables that need to be plotted, and filters to apply
var_1 = Select(title="Please select var on x axis", value="(select)", options=[], width=245, height=50, margin=(0,0,25,0))
var_2 = Select(title="Please select var on y axis", value="(select)", options=[], width=245, height=50, margin=(0,0,25,0))

range_prompt_x = Div(text='''Please select your range for x axis''')
range_prompt_y = Div(text='''Please select your range for y axis''')

add_filter_button = Button(label="Add more filters", button_type="primary")


def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2


# Callback for file_input
def upload_data(attr, old, new):
    # Read excel file into dataframe
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_excel(f, sheet_name='Sheet1_before_combining', engine='openpyxl')

    scatter_plot_data.upload_data(df)
    scatter_plot_data.preprocessing()

    # scatter_plot_data.debug_printing()

    # Update selection widget: variables to plot    
    var_1.options = scatter_plot_data.numeric_var
    var_2.options = scatter_plot_data.numeric_var

    # Update selection widget: filters
    first_filter_widget.options = scatter_plot_data.filter_list

    print('Dataset uploaded successfully')


def convert_bool(value_list):
    res = []
    for x in value_list:
        if (x == '0') or (x == '0.0'):
            res.append(False)
        elif (x == '1') or (x == '1.0'):
            res.append(True)

    return res if res != [] else value_list


def apply_filter(df):
    # print(filter_widgets.children)
    for c in filter_widgets.children:
        selected_filter = c.children[0].value
        if selected_filter == '(select)':
            continue
        selected_filter_values = c.children[1].value
        
        if selected_filter in scatter_plot_data.bool_list:
            if (selected_filter == 'tasks') or (selected_filter == 'subspec'):
                df = df[df[selected_filter_values].any(axis='columns')]
            else:
                selected_filter_values = convert_bool(selected_filter_values)
                df = df[df[selected_filter].isin(selected_filter_values)]
        elif selected_filter in scatter_plot_data.categ_list:
            df = df[df[selected_filter].isin(selected_filter_values)]
        else:
            print('Selected filter %s is neither bool nor categorical data, which should not happen', selected_filter)

    return df



# Callback for button_apply
def update_plot():
    plot_var_1 = str(var_1.value)
    plot_var_2 = str(var_2.value)

    if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
        button_apply.label = "Please re-select variables!"
        button_apply.button_type = "danger"  
    else:
        button_apply.label = "Generate your plot"
        button_apply.button_type = "primary"

        selected = pd.DataFrame(scatter_plot_data.source_backup.data)

        selected = apply_filter(selected)

        # Set x and y range, labels, function plot_settings in funcs.py
        plot_settings(plot, selected, plot_var_1, plot_var_2)

        selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
        scatter_plot_data.source.data = selected    

        # Create hover tool
        hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
        plot.add_tools(hover)


def edit_button(button, label, type):
    button.label = label
    button.button_type = type


def add_more_filters():

    total_options = scatter_plot_data.filter_list
    selected_options = []
    is_value_selected = True
    for c in filter_widgets.children:
            # print(c.children[0].value)
            # c is a row, where the first element is the filter widget, the second element is the value widget
            selected_options.append(c.children[0].value)
            is_value_selected = (is_value_selected and (c.children[0].value != '(select)'))

    if not is_value_selected:
        edit_button(add_filter_button, "Please reselect your filter or delete!", "danger")
    else:
        edit_button(add_filter_button, "Add more filters", "primary")
        options = [x for x in total_options if not x in selected_options]
        options.sort()
        if options == ['(select)']:
            edit_button(add_filter_button, "No more filters", "danger")
        else:
            new_filter_widget = Select(title='Please select your filter', value='(select)', options=options, width=150, height=70)
            delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 0, 0), )


            new_filter_widget.on_change('value', functools.partial(add_filter_value, widget=new_filter_widget))
            delete_button.on_click(functools.partial(delete_widget_and_button, widget=new_filter_widget))

            
            # Insert a row, where the first element is the filter widget, the second element will be the value widget
            filter_widgets.children.insert(0, row(new_filter_widget, delete_button))
              

def get_index_from_widget_list(widget_value):
    # print(filter_widgets.children)
    index = -1
    for i in range(len(filter_widgets.children)):
        if filter_widgets.children[i].children[0].value == widget_value:
            return i
    print('Failed to find in the widget list')
    return index

def delete_widget_and_button(widget):
    edit_button(add_filter_button, "Add more filters", "primary")
    delete_index = get_index_from_widget_list(widget.value)
    # print(filter_widgets.children[delete_index].children)
    filter_widgets.children.remove(filter_widgets.children[delete_index])
    for c in filter_widgets.children:
        c.children[0].options.append(widget.value)
        c.children[0].options.sort()

def add_filter_value(attr, old, new, widget):
  
   # If the filter is selected from scretch, remove the '(select)' option
    if old == '(select)':
        widget.options.remove('(select)')
    # If the selected filter changed, need to update other filter's options as well      
    for c in filter_widgets.children:
        if c.children[0] != widget:
            c.children[0].options.remove(new)
            if old != '(select)':
                c.children[0].options.append(old)
            c.children[0].options.sort()

    edit_button(add_filter_button, "Add more filters", "primary")
   
    df = pd.DataFrame(scatter_plot_data.source_backup.data)
    options=[]
    if new == 'tasks':
        options = scatter_plot_data.task_values
    elif new == 'subspec':
        options = scatter_plot_data.subspec_values
    elif new != '(select)':
        options = scatter_plot_data.get_column_from_name(df, new)
        options = [str(x) for x in options]
    
    widget_index = get_index_from_widget_list(new)
    if new == '(select)':
        new = ''
    num_of_widgets = len(filter_widgets.children[widget_index].children)
    if num_of_widgets == 3:
        filter_widgets.children[widget_index].children[1].title = new
        filter_widgets.children[widget_index].children[1].options = options
    elif num_of_widgets == 2:
        filter_value_widget = MultiSelect(title=new, value=[], options=options, height=70, width=150, description='Multi Select')
        filter_widgets.children[widget_index].children.insert(1, filter_value_widget)



file_input.on_change('value', upload_data)
add_filter_button.on_click(add_more_filters)

# Create a button widget for filters
button_apply = Button(label="Generate your plot", button_type="primary")
button_apply.on_click(update_plot)

# The first filter to be applied
first_filter_widget = Select(title='Please select your filter', value="(select)", options=[], width=150, height=70)
first_delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 0, 0))
first_delete_button.on_click(functools.partial(delete_widget_and_button, widget=first_filter_widget))
first_filter_widget.on_change('value', functools.partial(add_filter_value, widget=first_filter_widget))


filter_widgets = column(row(first_filter_widget, first_delete_button))



curdoc().add_root(row(column(upload_prompt, file_input, row(var_1, var_2), filter_widgets, add_filter_button, button_apply), plot))
