import pandas as pd
import numpy as np


def is_equal_two_list(list1, list2):

    if len(list1) == len(list2):
        is_same = all([x == y for x, y in zip(list1, list2)])
    else:
        is_same = False
    return is_same


def get_column_from_name(df, column_name):
    column_data = np.unique(df[column_name].tolist())
    column_data_no_nan = [x for x in column_data if str(x) != 'nan']

    return column_data_no_nan

def type_conversion(df):
    columns = list(df.columns.values)
    for c in columns:
        column_data_no_nan = get_column_from_name(df, c)
        # if is_equal_two_list(column_data_no_nan, [0., 1.]):
        #     df = df.astype({c: bool})
        if len(column_data_no_nan) >=2 and len(column_data_no_nan) <= 7:
            df = df.astype({c: 'category'})
        elif df[c].dtype == 'object':
            df = df.astype({c: 'string'})
        else:
            df = df.astype({c: 'float'})

    return df

##############################################################################
# Input(s):
#       df: dataframe from excel file
# Output(s):
#       df: dataframe after preprocessing
#       filter_values: in form list of list. contains selectable values from all filters
##############################################################################
def preprocess(df):
    
    column_names = list(df.columns.values)
    # Only keep the rows that have been recorded
    # Criteria: for a specific row, if all the values except column "Title" is not empty,
    #           then it means this row has been recorded.
    df = df.dropna(subset=list(set(column_names)-set(["Title", "year", "algo_neural_net"])), how='all')
    # print(df)
    df = type_conversion(df)
    # df = df.convert_dtypes()
   
    filter_values = df.select_dtypes(include=['category']).columns.tolist()
    task_filters = [x for x in filter_values if x.startswith('task')]
    for f in task_filters:
        df = df.astype({f: 'bool'})
    subspec_filters = [x for x in filter_values if x.startswith('subspec')]
    for f in subspec_filters:
        df = df.astype({f: 'bool'})
    # other_filters = [x for x in filter_values if (not x.startswith('task')) and (not x.startswith('subspec'))]

    # other_filters.insert(0, '(select)')
    numeric_var = df.select_dtypes(include=['float']).columns.tolist()
    numeric_var.insert(0, "(select)")
    

    return df, numeric_var

def get_all_filter_list(df):
    filter_values = df.select_dtypes(include=['category']).columns.tolist()
    filter_values.insert(0, 'subspecialities')
    filter_values.insert(0, 'tasks')
    filter_values.insert(0, "(select)")

    return filter_values

def get_task_list(df):
    filter_values = df.select_dtypes(include=['bool']).columns.tolist()
    task_filters = [x for x in filter_values if x.startswith('task')]
    
    return task_filters

def get_subspec_list(df):
    filter_values = df.select_dtypes(include=['bool']).columns.tolist()
    subspec_filters = [x for x in filter_values if x.startswith('subspec')]

    return subspec_filters



def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2
