import pandas as pd
import numpy as np

ml_task_text_dict = {'Binary classification': 0.0,
                'Multi-class classification': 1.0,
                'Regression': 2.0,
                'Segmentation': 3.0,
                'Clustering/unsupervised': 4.0,
                'Object detection': 5.0,
                'NLP': 6.0}

ml_task_code_dict = {'0.0': 'Binary classification',
                '1.0': 'Multi-class classification',
                '2.0': 'Regression',
                '3.0': 'Segmentation',
                '4.0': 'Clustering/unsupervised',
                '5.0': 'Object detection',
                '6.0': 'NLP'}

data_text_dict = {'No': 0.0,
                'Yes': 1.0,
                'Upon request': 2.0}

data_code_dict = {'0.0': 'No',
                  '1.0': 'Yes',
                  '2.0': 'Upon request'}

gender_text_dict = {'Female': 0.0,
                   'Male': 1.0,
                   'Mixed': 2.0,
                   'Not specified': 3.0}

gender_code_dict = {'0.0': 'Female',
                    '1.0': 'Male',
                    '2.0': 'Mixed',
                    '3.0': 'Not specified'}

def is_equal_two_list(list1, list2):

    if len(list1) == len(list2):
        is_same = all([x == y for x, y in zip(list1, list2)])
    else:
        is_same = False
    return is_same


def type_conversion(df):
    columns = list(df.columns.values)
    # print(columns)
    for c in columns:
        if df[c].dtype == np.float64 or df[c].dtype == np.int64 or df[c].dtype == np.float32 or df[c].dtype == np.int32:        
            column_list = np.unique(df[c].tolist())
            column_list = [x for x in column_list if ~np.isnan(x)]

            if is_equal_two_list(column_list, [0., 1.]):
                df = df.astype({c: bool})
            else:
                if len(column_list) >= 2 and len(column_list) < 10:
                    df = df.astype({c: 'category'})
        elif df[c].dtype == 'object':
            df = df.astype({c: 'string'})

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
    # print(df.dtypes)

    filter_values = df.select_dtypes(include=['category', 'bool']).columns.tolist()
    task_filters = [x for x in filter_values if x.startswith('task')]
    subspec_filters = [x for x in filter_values if x.startswith('subspec')]
    other_filters = [x for x in filter_values if (not x.startswith('task')) and (not x.startswith('subspec'))]
    numeric_var = df.select_dtypes(include=['float']).columns.tolist()
    numeric_var.insert(0, "(select)")
    

    return df, task_filters, subspec_filters, other_filters, numeric_var

def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2


def code_2_text(column_name, value):
    try:        
        if column_name == "ml_task_description":
            value = ml_task_code_dict[value]
        if column_name == "raw data availability":
            value = data_code_dict[value]
        if column_name == "processed data availability":
            value = data_code_dict[value]
        if column_name == "gender":
            value = gender_code_dict[value]
    except:
        print('Somethings wrong in code_2_text')

    return value


def text_2_code(column_name, value):

    try:        
        if column_name == "ml_task_description":
            value = ml_task_text_dict[value]
        if column_name == "raw data availability":
            value = data_text_dict[value]
        if column_name == "processed data availability":
            value = data_text_dict[value]
        if column_name == "gender":
            value = gender_text_dict[value]
    except:
        print('Somethings wrong in text_2_code')

    return value
