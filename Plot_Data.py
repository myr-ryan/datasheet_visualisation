from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd


class Plot_Data:
    # Class variables
    column_names = []
    filter_list = []
    # value_list = []
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
        if column_name == 'task':
            return self.task_values
        elif column_name == 'subspec':
            return self.subspec_values
        else:
            column_data = np.unique(df[column_name].tolist())
            column_data_no_nan = [x for x in column_data if str(x) != 'nan']
            # If the column is the categorical data that need to be converted from brackets (e.g. ['MobileNet'] -> MobileNet)
            if ((str(column_data_no_nan[0]).startswith('[')) and (str(column_data_no_nan[0]).endswith(']'))) or ((str(column_data_no_nan[-1]).startswith('[')) and (str(column_data_no_nan[-1]).endswith(']'))):
                # column_data_no_nan = [list(x) for x in column_data_no_nan]
                for i in range(len(column_data_no_nan)):
                    column_data_no_nan[i] = column_data_no_nan[i].replace('[', '')
                    column_data_no_nan[i] = column_data_no_nan[i].replace(']', '')
                    column_data_no_nan[i] = column_data_no_nan[i].replace('\'', '')
                    column_data_no_nan[i] = column_data_no_nan[i].split(', ')

                # column_data_no_nan = [x.replace('[', '') for x in column_data_no_nan]
                return np.unique([x for sublist in column_data_no_nan for x in sublist])
                # print(column_data_no_nan)
            else:
                return column_data_no_nan
        # return column_data_no_nan


    def type_conversion(self, df):
        for c in self.column_names:
            
            if df[c].dtype != 'datetime64[ns]':
                column_data_no_nan = self.get_column_from_name(df, c)
                if len(column_data_no_nan) == 1:
                    if column_data_no_nan == [1] or column_data_no_nan == [1.0] or column_data_no_nan == [0] or column_data_no_nan == [0.0]:
                        df = df.astype({c: bool})
                    else:
                        df = df.astype({c: 'string'})
                elif len(column_data_no_nan) >= 2 and len(column_data_no_nan) < 12:    
                    if self.is_equal_two_list(column_data_no_nan, [0., 1.]) or (self.is_equal_two_list(column_data_no_nan, [0, 1])):
                        df = df.astype({c: bool})
                    else:
                        if ('specify' in df[c].name) or ('comment' in df[c].name):
                            df = df.astype({c: 'string'})
                        else:
                            df = df.astype({c: 'category'})
                else:
                    if df[c].dtype == 'object':
                        if (str(df[c][0]).startswith('[')) and (str(df[c][0]).endswith(']')):
                            df = df.astype({c: 'category'})
                        else:
                            df = df.astype({c: 'string'})          
                    # int or float
                    else:
                        df = df.astype({c: 'float'})

        return df


    def upload_data(self, df):
          
        self.source.data = df
        # print(self.source.data)
        # This is a bokeh issue, it will take index in the dataframe as seperate column, which will cause issue afterwards
        self.source.remove('index')
        self.source_backup.data = df
        self.source_backup.remove('index')

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
    #         elif f == 'task':
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


    def bol_to_cat(self, df, new_column_name, columns):

        cols_to_cat = df.loc[:, columns]
        df.drop(columns, axis=1, inplace=True)
        cols_to_cat = pd.DataFrame({new_column_name: cols_to_cat.columns[np.where(cols_to_cat)[1]]}, np.where(cols_to_cat)[0])  

        # left join by default
        df = cols_to_cat.join(df)
        df.reset_index(drop=True, inplace=True)
        

        return df



    def preprocessing(self):
        df = pd.DataFrame(self.source.data)
        # print(df.shape[0])
        df = df.dropna(subset=['ml_task_description'], how='all')
        df.drop(['subspec_gynonc'], axis=1, inplace=True)

        self.column_names = list(df.columns.values)
        # print(df.shape[0])
        # print(df[df['raw data availability'].isna()])
        # for x in df[df['raw data availability'].isna()]:
        #     print(x)
        # print(df['raw data availability'])

        df = self.type_conversion(df)     

    
        self.bool_list = df.select_dtypes(include=['bool']).columns.tolist()


        # all_categorical_bool = df.select_dtypes(include=['category', 'bool']).columns.tolist()
        self.task_values = [x for x in self.bool_list if x.startswith('task')]
        self.subspec_values = [x for x in self.bool_list if x.startswith('subspec')]
        self.bool_list = [x for x in self.bool_list if (not x.startswith('task')) and (not x.startswith('subspec'))]

        self.categ_list = df.select_dtypes(include=['category']).columns.tolist()
        self.categ_list.insert(0, 'subspec')
        self.categ_list.insert(0, 'task')
        self.categ_list.insert(0, "(select)")
        self.categ_list.sort()

        self.filter_list = self.categ_list + self.bool_list
        # self.filter_list.insert(0, "(select)")
        # self.filter_list.sort()

        self.bool_list.insert(0, "(select)")
        self.bool_list.sort()

        # self.get_value_list()

        self.numeric_var = df.select_dtypes(include=['float']).columns.tolist()
        self.numeric_var.insert(0, "(select)")

        # boolean columns to categorical columns
        df = self.bol_to_cat(df, 'task', self.task_values)
        df = self.bol_to_cat(df, 'subspec', self.subspec_values)
        # print(df)


        # This is a bokeh issue, it will take index in the dataframe as seperate column, which will cause issue afterwards
        self.source.data = df
        self.source.remove('index')
        self.source_backup.data = df
        self.source_backup.remove('index')
        # print(pd.DataFrame(self.source.data))
        # print(pd.DataFrame(self.source_backup.data).columns)



    def debug_printing(self):
        pass
        # print('Column names are: ', self.column_names)
        # print('Filter list (categorical + boolean): ', self.filter_list)
        # print('Bool list: ', self.bool_list)
        # print('Task list: ', self.task_values)
        # print('Subspec list: ', self.subspec_values)
        # print('Numerical list: ', self.numeric_var)

