import pandas as pd
import numpy as np


# Inputs:
#       df: dataframe from excel file
#       
def preprocess(df, filter_values):
    
    # Only keep the rows that have been recorded
    df = df.dropna(subset=["ml_task_description", "data_units", "data_size_all", "raw data availability"], how='all')

    # for f in filters:
    #     filter_values.append(list(set(df[f].tolist())))

    # TODO
    filter_values.append(list(set(df['data_units'].tolist())))
    filter_values.append(list(set(df['raw data availability'].tolist())))
    filter_values.append(list(set(df['processed data availability'].tolist())))
    
    print(len(filter_values[0]))
    print(filter_values) 

    

    return df