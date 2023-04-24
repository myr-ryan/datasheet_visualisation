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
# source = ColumnDataSource(data=empty_data)
# source_backup = ColumnDataSource(data=empty_data)

# x_range=source.data["Paper ID"]
plot = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
plot.scatter('x', 'y', source=scatter_plot_data.source)
# scatter = Scatter(x="Paper ID", y="y", marker="circle")
# plot.add_glyph(source, scatter)


# file_input = FileInput(accept='.xlsx', width=400)
file_input = FileInput(accept='.xlsx')


# Filters that you can apply on the plotting results, hard coded for now
# filters = ['data_units', 'raw data availability', 'processed data availability', 'task', 'subspec', 'sample type']


# Set up widgets for variables that need to be plotted, and filters to apply
var_1 = Select(title="Please select var on x axis", value="(select)", options=[])
var_2 = Select(title="Please select var on y axis", value="(select)", options=[])




add_filter_button = Button(label="Add more filters", button_type="primary")


##############################################################################
# Input(s):
#       df: dataframe to be filtered
#       widget: the binary selection widget to be applied
# Output(s):
#       df: dataframe after filtering
##############################################################################
def apply_bi_filter(df, widget):

    selected_list = widget.active
    if selected_list:
        column_names = [widget.labels[x] for x in selected_list]
        df = df[df[column_names].any(axis='columns')]
    
    return df



def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2

##############################################################################
# Input(s):
#       df: dataframe to be filtered
#       widget: the mixed (binary + categorical) selection widget to be applied
# Output(s):
#       df: dataframe after filtering
##############################################################################
# def apply_mixed_filter(df, widget):
#     selected_list = widget.active

#     for f in selected_list:        
#         column_name = others_widget.labels[f]             
        
#         # Check if the filter is categorical data
#         is_category = (df[column_name].dtype == 'category')

#         if is_category:
#             f_value = []
#             for value_widget in widgets.children[1].children:
#                 if value_widget.title == column_name:
#                     f_value = value_widget.value
#                     # f_value = [text_2_code(column_name, x) for x in f_value]
                
#             if f_value:
#                 df = df[df[column_name].isin(f_value)]

#         else:
#             # df = pd.DataFrame(source_backup.data)
#             df = df[df[column_name]]    

#     return df      

##############################################################################
# Input(s):
#       short: the shorter list of indices from widget.active
#       long: the longer list of indices from widget.active
# Output(s):
#       column_name: the name of the column selected/unselected
##############################################################################
# def find_col_from_index(short, long):
#     short = set(short)
#     column_index = [x for x in long if x not in short][0]
#     column_name = others_widget.labels[column_index]  

#     return column_name

# Callback for file_input
def upload_data(attr, old, new):
    # Read excel file into dataframe
    decoded = base64.b64decode(new)
    f = io.BytesIO(decoded)
    df = pd.read_excel(f, sheet_name='Sheet1_before_combining', engine='openpyxl')

    scatter_plot_data.upload_data(df)
    scatter_plot_data.preprocessing()

    # scatter_plot_data.debug_printing()

    # Function 'preprocess' in file funcs.py
    # Returns:
    #       df: dataframe with modified data types, 
    #       task_filters, subspec_filters, other_filters: filters to be applied (categorical and boolean data)
    #       numeric_var: data to be plotted (numerical data) 
    # df, numeric_var = preprocess(df)

    # print(df["task_other ( specify)"][10])
    # Update selection widget: variables to plot    
    var_1.options = scatter_plot_data.numeric_var
    var_2.options = scatter_plot_data.numeric_var

    # Update selection widget: filters
    first_filter_widget.options = scatter_plot_data.filter_list

    # Update source data, source_backup is created for reselection purpose
    

    # source.data = df
    # source_backup.data = df
    print('Dataset uploaded successfully')

def apply_filter(df):
    # print(filter_widgets.children)
    for c in filter_widgets.children:
        print(scatter_plot_data.task_values)
        print(scatter_plot_data.subspec_values)
        print(scatter_plot_data.filter_list)

        # 

        selected_filter_value = c.children[0].value

        if (selected_filter_value in scatter_plot_data.task_values) or (selected_filter_value in scatter_plot_data.subspec_values):
            df = df[df[selected_filter_value].any(axis='columns')]
        elif selected_filter_value in scatter_plot_data.value_list:
            df = df[df[column_name].isin(f_value)]

    return df



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

        selected = pd.DataFrame(scatter_plot_data.source_backup.data)

        # selected = apply_filter(selected)

        # # Apply filter for task
        # selected = apply_bi_filter(selected, task_widget)
        # # Apply filter for subspecies
        # selected = apply_bi_filter(selected, subspec_widget)
        # # Apply filter for others
        # selected = apply_mixed_filter(selected, others_widget)

        # Set x and y range, labels, function plot_settings in funcs.py
        plot_settings(plot, selected, plot_var_1, plot_var_2)

        selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
        scatter_plot_data.source.data = selected    

        # Create hover tool
        hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
        plot.add_tools(hover)


# Inputs:
#       attr
#       old: includes all values in argument 'active' in 'others_widget' CheckBox before checking, values are indices of selected filters, e.g. [0, 1]
#       new: includes all values in argument 'active' in 'others_widget' CheckBox after checking, values are indices of selected filters, e.g. [0, 1, 2]
# def update_filter(attr, old, new):


    # # if add a filter
    # if len(new) > len(old):
    #     # Find the selected filter
    #     column_name = find_col_from_index(old, new)

    #     # Only make changes when dealing with categorical data
    #     is_category = (source.data[column_name].dtype == 'category')
    #     if is_category:
        
    #         df = pd.DataFrame(source_backup.data)
    #         options = df[column_name]
    #         options = list(map(str, list(set(options.tolist()))))
    #         # options = [code_2_text(column_name, x) for x in options]

    #         selectable_values = MultiChoice(title=column_name, value=[], options=options)
    #         widgets.children[1].children.insert(0, selectable_values)
                            
    #     # if unselect/remove a filter
    # else:
    #     # Find the unselected/removed filter
    #     column_name = find_col_from_index(new, old)

    #     # Only make changes when dealing with categorical data
    #     is_category = (source.data[column_name].dtype == 'category')
    #     if is_category:
            
    #         # Delete the unselected/removed filter widget
    #         for value_widget in widgets.children[1].children:
    #             if value_widget.title == column_name:
    #                 widgets.children[1].children.remove(value_widget)
def edit_button(button, label, type):
    button.label = label
    button.button_type = type


def add_more_filters():

    # new_filter_widget = Select(title='Please select your filter', value='(select)', options=new_option_list)
    # filter_value_list, value_list = get_all_value(filter_list)
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
        # options = get_rest_options(total_options, selected_options)  
        options = [x for x in total_options if not x in selected_options]
        options.sort()
        # new_option_list = list(set(total_options)-set(selected_options))
        if options == []:
            edit_button(add_filter_button, "No more filters", "danger")
        else:
            new_filter_widget = Select(title='Please select your filter', value='(select)', options=options)
            delete_button = Button(label="Delete", button_type="primary")


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
    # filter_widgets.children[delete_index].children.remove(filter_widgets.children[delete_index].children)



# def remove_select(attr, old, new, widget):
#     widget.options = [x for x in widget.options if not x in ['(select)']]
    # widget.options = list(set(widget.options) - set(['(select)']))


def add_filter_value(attr, old, new, widget):
  
   # If the filter is selected from scretch, remove the '(select)' option
    if old != '(selected)':
        widget.options.remove('(select)')
    # If the selected filter changed, we need to update other filter's options as well
    else:      
        for c in filter_widgets.children:
            if c.children[0] != widget:
                c.children[0].options.remove(new)
                c.children[0].options.append(old)
                c.children[0].options.sort()

    edit_button(add_filter_button, "Add more filters", "primary")
   
    df = pd.DataFrame(scatter_plot_data.source_backup.data)
    options=[]
    if new == 'tasks':
        options = scatter_plot_data.task_values
    elif new == 'subspecialities':
        options = scatter_plot_data.subspec_values
    elif new != '(select)':
        options = scatter_plot_data.get_column_from_name(df, new)
    
    widget_index = get_index_from_widget_list(new)
    if new == '(select)':
        new = ''
    num_of_widgets = len(filter_widgets.children[widget_index].children)
    if num_of_widgets == 3:
        filter_widgets.children[widget_index].children[1].title = new
        filter_widgets.children[widget_index].children[1].options = options
    elif num_of_widgets == 2:
        filter_value_widget = MultiSelect(title=new, value=[], options=options, height=70, width=200, description='Multi Select')
        filter_widgets.children[widget_index].children.insert(1, filter_value_widget)



file_input.on_change('value', upload_data)
add_filter_button.on_click(add_more_filters)

# Create a button widget for filters
button_apply = Button(label="Generate", button_type="primary")
button_apply.on_click(update_plot)

# The first filter to be applied
first_filter_widget = Select(title='Please select your filter', value="(select)", options=[])
first_delete_button = Button(label="Delete", button_type="primary")
first_delete_button.on_click(functools.partial(delete_widget_and_button, widget=first_filter_widget))
first_filter_widget.on_change('value', functools.partial(add_filter_value, widget=first_filter_widget))


filter_widgets = column(row(first_filter_widget, first_delete_button))



curdoc().add_root(column(file_input, row(var_1, var_2), add_filter_button, filter_widgets, button_apply, plot))

