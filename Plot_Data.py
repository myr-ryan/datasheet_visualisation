from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd


class Plot_Data:
    # Class variables
    column_names = []
    filter_list = []
    value_list = []
    filter_value_list = []
    task_values = []
    subspec_values = []
    numeric_var = []


    def __init__(self, data):
        self.source = ColumnDataSource(data=data)
        self.source_backup = ColumnDataSource(data=data)

    def get_column_from_name(self, df, column_name):
        column_data = np.unique(df[column_name].tolist())
        column_data_no_nan = [x for x in column_data if str(x) != 'nan']
        return column_data_no_nan


    def type_conversion(self, df):
        for c in self.column_names:
            column_data_no_nan = self.get_column_from_name(df, c)
            # if is_equal_two_list(column_data_no_nan, [0., 1.]):
            #     df = df.astype({c: bool})
            if len(column_data_no_nan) >=2 and len(column_data_no_nan) <= 7:
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

    def add_indent(self, list):
        res = []
        for l in list:
            res.append("*   " + str(l))
        return res

    def get_value_list(self):
        df = pd.DataFrame(self.source.data)

        for f in self.filter_list:
            self.filter_value_list.append(f)
            if f == '(select)':
                values_with_indent = []
            elif f == 'tasks':
                self.value_list.append(self.task_values)
                values_with_indent = self.add_indent(self.task_values)          
            elif f == 'subspecialities':
                self.value_list.append(self.subspec_values)
                values_with_indent = self.add_indent(self.subspec_values)
            else:
                values = self.get_column_from_name(df, f)
                self.value_list.append(values)
                values_with_indent = self.add_indent(values)

            for v in values_with_indent:
                self.filter_value_list.append(v)



    def preprocessing(self):
        df = pd.DataFrame(self.source.data)
        df = df.dropna(subset=list(set(self.column_names)-set(["Title", "year", "algo_neural_net"])), how='all')

        df = self.type_conversion(df)
        self.source.data = df

        all_categorical = df.select_dtypes(include=['category']).columns.tolist()
        self.task_values = [x for x in all_categorical if x.startswith('task')]
        for f in self.task_values:
            df = df.astype({f: 'bool'})
        self.subspec_values = [x for x in all_categorical if x.startswith('subspec')]
        for f in self.subspec_values:
            df = df.astype({f: 'bool'})
        
        self.filter_list = df.select_dtypes(include=['category']).columns.tolist()
        self.filter_list.insert(0, 'subspecialities')
        self.filter_list.insert(0, 'tasks')
        self.filter_list.insert(0, "(select)")

        self.get_value_list()

        self.numeric_var = df.select_dtypes(include=['float']).columns.tolist()
        self.numeric_var.insert(0, "(select)")


    # def get_all_values(self, )


    def debug_printing(self):
        # print(self.column_names)
        print(self.filter_list)
        print(self.value_list)
        print(self.filter_value_list)
        # print(self.task_values)
        # print(self.subspec_values)
        # print(self.numeric_var)

