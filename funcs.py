import pandas as pd
import numpy as np


def type_conversion(df):
    def astype_conv(df, column_name, conv_type):
        try:
            df = df.astype({column_name: conv_type})
        except:
            print("Please check column: ", column_name)
        return df

    df = astype_conv(df, "Paper ID", int)
    df = astype_conv(df, "Title", str)
    df = astype_conv(df, "ml_task_description", int)
    df = astype_conv(df, "data_units", str)
    df = astype_conv(df, "data_size_all", float)
    df = astype_conv(df, "data_size_validation", float)
    df = astype_conv(df, "data_size_testing", float)
    df = astype_conv(df, "data_size_training", float)
    df = astype_conv(df, "explainability", str)
    df = astype_conv(df, "balanced", bool)
    df = astype_conv(df, "balanced_comment", str)
    df = astype_conv(df, "bias", str)
    df = astype_conv(df, "class_labels", str)
    df = astype_conv(df, "data_source", str)
    df = astype_conv(df, "data_links", str)
    df = astype_conv(df, "raw data availability", int)
    df = astype_conv(df, "processed data availability", int)
    df = astype_conv(df, "gender", int)
    df = astype_conv(df, "age specified", str)
    df = astype_conv(df, "task_detection", bool)
    df = astype_conv(df, "task_diagnosis", bool)
    df = astype_conv(df, "task_prognosis", bool)
    df = astype_conv(df, "treatment design (monitoring, planning)", bool)
    df = astype_conv(df, "treatment design comment", str)
    df = astype_conv(df, "task_risk prediction", bool)
    df = astype_conv(df, "task_subtyping", bool)
    df = astype_conv(df, "task_other ( specify)", str)
    df = astype_conv(df, "subspec_ovarian", bool)
    df = astype_conv(df, "subspec_cervical", bool)
    df = astype_conv(df, "subspec_endometrial", bool)
    df = astype_conv(df, "subspec_metastasis", bool)
    df = astype_conv(df, "subspec_other (specify)", bool)
    df = astype_conv(df, "performance_auc", float)
    df = astype_conv(df, "performance_precision (PPV)", float)
    df = astype_conv(df, "performance_specificity", float)
    df = astype_conv(df, "performance_NPV", float)
    df = astype_conv(df, "performance_sensitivity (recall)", float)
    df = astype_conv(df, "performance_F1", float)
    df = astype_conv(df, "performance_accuracy", float)
    df = astype_conv(df, "neural network type", str)
    df = astype_conv(df, "data collection technology", str)
    df = astype_conv(df, "algorithm-pipeline", str)
    df = astype_conv(df, "sample type", str)

    return df


# Inputs:
#       df: dataframe from excel file
# Outputs:
#       df: dataframe after preprocessing
#       filter_values: in form list of list. contains selectable values from all filters
def preprocess(df):
    
    column_names = list(df.columns.values)
    # Only keep the rows that have been recorded
    # Criteria: for a specific row, if all the values except column "Title" is not empty,
    #           then it means this row has been recorded.
    df = df.dropna(subset=list(set(column_names)-set(["Title", "year", "algo_neural_net"])), how='all')
    df = type_conversion(df)


    # TODO
    
    filter_values = []
    filter_values.append(list(set(df['data_units'].tolist())))
    filter_values[0].insert(0, "All")
    # filter_values.append(list(set(df['raw data availability'].tolist())))
    # filter_values.append(list(set(df['processed data availability'].tolist())))
    
    # print(len())
    # print(filter_values) 

    

    return df, filter_values

def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2

        