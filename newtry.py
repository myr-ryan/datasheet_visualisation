from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from bokeh.models import ColumnDataSource, Button, ColorPicker, HoverTool, DateRangeSlider, MultiChoice, CheckboxGroup, Div
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
# filters = ['data_units', 'raw data availability', 'processed data availability', 'task', 'subspec', 'sample type']


# Set up widgets for variables that need to be plotted, and filters to apply
var_1 = Select(title="Please select var on x axis", value="(select)", options=[])
var_2 = Select(title="Please select var on y axis", value="(select)", options=[])


# filter_text = Div(text='''Select filter:''')
filter_widget = Select(title='Please select your filter', value="(select)", options=[])

add_filter_button = Button(label="Add more filters", button_type="primary")
# task_text = Div(text='''Select task:''')
# task_widget = CheckboxGroup(name='Tasks', labels=[], active=[])

# subspec_text = Div(text='''Select subspecies:''')
# subspec_widget = CheckboxGroup(name='Subspec', labels=[], active=[])

# others_text = Div(text='''Select other options:''')
# others_widget = CheckboxGroup(name='Filters', labels=[], active=[])

# num_text = Div(text='''Select range:''')


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
    df = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')

    # Function 'preprocess' in file funcs.py
    # Returns:
    #       df: dataframe with modified data types, 
    #       task_filters, subspec_filters, other_filters: filters to be applied (categorical and boolean data)
    #       numeric_var: data to be plotted (numerical data) 
    df, task_filters, subspec_filters, other_filters, numeric_var = preprocess(df)

    # print(df["task_other ( specify)"][10])
    # Update selection widget: variables to plot    
    var_1.options = numeric_var
    var_2.options = numeric_var

    # Update selection widget: filters
    filter_widget.options = other_filters

    # task_widget.labels = task_filters
    # subspec_widget.labels = subspec_filters
    # others_widget.labels = other_filters

    # Update source data, source_backup is created for reselection purpose
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

        selected = pd.DataFrame(source_backup.data)

        # # Apply filter for task
        # selected = apply_bi_filter(selected, task_widget)
        # # Apply filter for subspecies
        # selected = apply_bi_filter(selected, subspec_widget)
        # # Apply filter for others
        # selected = apply_mixed_filter(selected, others_widget)

        # Set x and y range, labels, function plot_settings in funcs.py
        plot_settings(plot, selected, plot_var_1, plot_var_2)

        selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
        source.data = selected    

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
    total_options = filter_widget.options
    selected_options = []
    is_first_value_selected = (filter_widget.value != '(select)')
    if is_first_value_selected:
        selected_options.append(filter_widget.value)
    
    is_other_value_selected = True
    if additional_filter_widget.children != []:
        is_other_value_selected = (additional_filter_widget.children[0].value != '(select)')
    for c in additional_filter_widget.children:
        selected_options.append(c.value)

    if ((not is_first_value_selected) or (not is_other_value_selected)):
        edit_button(add_filter_button, "Please select your last filter!", "danger")
    else:
        edit_button(add_filter_button, "Add more filters", "primary")

        new_option_list = list(set(total_options)-set(selected_options))
        if new_option_list == ['(select)']:
            edit_button(add_filter_button, "No more filters", "danger")
        else:
            new_filter_widget = Select(title='Please select your filter', value="(select)", options=new_option_list)

            additional_filter_widget.children.insert(0, row(new_filter_widget))

# def add_filter_value():
    # selected_filter = filter_widget.value
    # filter_value = Select(title=selected_filter, value="")
    # first_filter_widget.children.insert(-1, )



file_input.on_change('value', upload_data)

filter_widget.on_change('active', add_filter_value)

add_filter_button.on_click(add_more_filters)




# Create a button widget for filters
button_apply = Button(label="Generate", button_type="primary")
button_apply.on_click(update_plot)


first_filter_widget = row(filter_widget)
additional_filter_widget = column()

curdoc().add_root(column(file_input, row(var_1, var_2), first_filter_widget, add_filter_button, additional_filter_widget, button_apply, plot))

