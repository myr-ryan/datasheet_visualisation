from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd


class Plot_Data:
    # Class variables
    column_names = []
    filter_list = []
    value_list = []
    # filter_value_list = []
    task_values = []
    subspec_values = []
    numeric_var = []
    bool_list = []
    categ_list = []


    def __init__(self, data):
        self.source = ColumnDataSource(data=data)
        self.source_backup = ColumnDataSource(data=data)

    
    def is_equal_two_list(self, list1, list2):

        if len(list1) == len(list2):
            is_same = all([x == y for x, y in zip(list1, list2)])
        else:
            is_same = False
        return is_same

    def get_column_from_name(self, df, column_name):
        column_data = np.unique(df[column_name].tolist())
        column_data_no_nan = [x for x in column_data if str(x) != 'nan']
        return column_data_no_nan


    def type_conversion(self, df):
        for c in self.column_names:
            column_data_no_nan = self.get_column_from_name(df, c)
            if self.is_equal_two_list(column_data_no_nan, [0., 1.]):
                df = df.astype({c: bool})
            elif len(column_data_no_nan) >=2 and len(column_data_no_nan) <= 7:
                df = df.astype({c: 'category'})
            elif df[c].dtype == 'object':
                df = df.astype({c: 'string'})
            else:
                df = df.astype({c: 'float'})

        return df


    def upload_data(self, df):
        self.column_names = list(df.columns.values)      
        self.source.data = df
        self.source_backup.data = df

    # deprecated
    # def add_indent(self, list):
    #     res = []
    #     for l in list:
    #         res.append("*   " + str(l))
    #     return res

    # # deprecated
    # def get_value_list(self):
    #     df = pd.DataFrame(self.source.data)
    #     for f in self.filter_list:
    #         # self.filter_value_list.append(f)
    #         if f == '(select)':
    #             values_with_indent = []
    #         elif f == 'tasks':
    #             self.value_list.append(self.task_values)
    #             values_with_indent = self.add_indent(self.task_values)          
    #         elif f == 'subspec':
    #             self.value_list.append(self.subspec_values)
    #             values_with_indent = self.add_indent(self.subspec_values)
    #         else:
    #             values = self.get_column_from_name(df, f)
    #             self.value_list.append(values)
    #             values_with_indent = self.add_indent(values)

    #         for v in values_with_indent:
    #             self.filter_value_list.append(v)



    def preprocessing(self):
        df = pd.DataFrame(self.source.data)
        df = df.dropna(subset=list(set(self.column_names)-set(["Title", "year", "algo_neural_net"])), how='all')

        df = self.type_conversion(df)
        self.source.data = df

        self.bool_list = df.select_dtypes(include=['bool']).columns.tolist()


        # all_categorical_bool = df.select_dtypes(include=['category', 'bool']).columns.tolist()
        self.task_values = [x for x in self.bool_list if x.startswith('task')]
        self.subspec_values = [x for x in self.bool_list if x.startswith('subspec')]
        self.bool_list = [x for x in self.bool_list if (not x.startswith('task')) and (not x.startswith('subspec'))]
        self.bool_list.insert(0, 'subspec')
        self.bool_list.insert(0, 'tasks')

        self.categ_list = df.select_dtypes(include=['category']).columns.tolist()
        self.filter_list = self.categ_list + self.bool_list
        self.filter_list.insert(0, "(select)")
        self.filter_list.sort()

        # self.get_value_list()

        self.numeric_var = df.select_dtypes(include=['float']).columns.tolist()
        self.numeric_var.insert(0, "(select)")



    def debug_printing(self):
        # print(self.column_names)
        print(self.filter_list)
        # print(self.value_list)
        print(self.bool_list)
        # print(self.filter_value_list)
        print(self.task_values)
        print(self.subspec_values)
        # print(self.numeric_var)

