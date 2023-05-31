from bokeh.models.widgets import Select, FileInput, Button, RangeSlider, MultiSelect, NumericInput
from bokeh.models import Div, HoverTool
import base64
import io
import pandas as pd
import functools
from bokeh.layouts import column, row
from General_plot_helper import *
from bokeh.palettes import d3
from bokeh.models import CategoricalColorMapper
import numpy as np


# Widgets and plot settings for all plots

class GeneralPlot:
    selected_color_stra = '(select)'
    
    def cb_color_select(self, attr, old, new):
        self.selected_color_stra = new


    # def cb_upload(self, attr, old, new):
    #     # Read excel file into dataframe
    #     decoded = base64.b64decode(new)
    #     f = io.BytesIO(decoded)
    #     df = pd.read_excel(f, sheet_name='Sheet1_before_combining', engine='openpyxl')

    #     self.plot_data.upload_data(df)
    #     self.plot_data.preprocessing()

    #     # plot specific
    #     # for w in self.plot_spec_select_widgets.children:
    #     #     w.options = self.numeric_var_ops
        
    #     # Update the first filter widget
    #     self.first_filter_select_widget.options = self.filter_list_ops

    #     # Update the first range slider
    #     self.first_range_select_widget.options = self.numeric_var_ops
    
    def edit_button(self, button, label, type):
        button.label = label
        button.button_type = type


    def cb_add_filter_button(self):
        total_options = self.filter_list_ops
        
        selected_options = []
        is_value_selected = True
        for c in self.filter_widgets.children:
                # c is a row, where the first element is the filter widget, the second element is the value widget
                selected_options.append(c.children[0].value)
                is_value_selected = (is_value_selected and (c.children[0].value != '(select)'))

        if not is_value_selected:
            self.edit_button(self.add_filter_button_widget, "Please reselect your filter or delete!", "danger")
        else:
            self.edit_button(self.add_filter_button_widget, "Add more filters", "primary")
            options = [x for x in total_options if not x in selected_options]
            options.sort()
            if options == ['(select)']:
                self.edit_button(self.add_filter_button_widget, "No more filters", "danger")
            else:
                new_filter_widget = Select(title='Please select your filter', value='(select)', options=options, width=150, height=70)
                new_filter_delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 0, 0))


                new_filter_widget.on_change('value', functools.partial(self.cb_filter_value, widget=new_filter_widget))
                new_filter_delete_button.on_click(functools.partial(self.cb_delete, w_type='filters', add_button=self.add_filter_button_widget, widget=new_filter_widget))

                # Insert a row, where the first element is the filter widget, the second element will be the value widget
                self.filter_widgets.children.insert(0, row(new_filter_widget, new_filter_delete_button))

    def cb_add_range_button(self):
        total_options = self.numeric_var_ops
        selected_options = []
        is_value_selected = True
        # print(self.range_selectors.children)
        for c in self.range_selectors.children:
                # print(c.children[0].children[0].value)
                # c is a row, where the first element is the filter widget, the second element is the value widget
                selected_options.append(c.children[0].children[0].value)
                is_value_selected = (is_value_selected and (c.children[0].children[0].value != '(select)'))
        
        if not is_value_selected:
            self.edit_button(self.add_range_button_widget, "Please reselect your range or delete!", "danger")
        else:
            self.edit_button(self.add_range_button_widget, "Add more ranges", "primary")
            options = [x for x in total_options if not x in selected_options]
            options.sort()
            if options == ['(select)']:
                self.edit_button(self.add_filter_button_widget, "No more ranges", "danger")
            else:
                
                new_range_select_widget = Select(title='Please select your variable', value="(select)", options=options, width=170, height=50)
                new_range_widget = RangeSlider(start=0, end=1, value=(0,1), title="", width=370)
                new_range_delete_button = Button(label="Delete this range", button_type="primary", width=50, height=30, margin=(15, 0, 0, 0))
                new_range_min_widget = NumericInput(value=0, low=0, high=1, title="min")
                new_range_max_widget = NumericInput(value=0, low=0, high=1, title="max")

              
                new_range_select_widget.on_change('value', functools.partial(self.cb_range_select, select=new_range_select_widget, slider=new_range_widget, min_widget=new_range_min_widget, max_widget=new_range_max_widget))                                                     
                new_range_widget.on_change('value', functools.partial(self.cb_range, min_widget=new_range_min_widget, max_widget=new_range_max_widget))
                new_range_min_widget.on_change('value', functools.partial(self.cb_range_text, slider=new_range_widget, widget=new_range_min_widget))
                new_range_max_widget.on_change('value', functools.partial(self.cb_range_text, slider=new_range_widget, widget=new_range_max_widget))
                new_range_delete_button.on_click(functools.partial(self.cb_delete, w_type='ranges', add_button=self.add_range_button_widget, widget=new_range_select_widget))

                # Insert
                self.range_selectors.children.insert(0, column(row(new_range_select_widget, new_range_min_widget, new_range_max_widget), row(new_range_widget, new_range_delete_button)))


    def bool_to_str(self, value_list):
        if len(value_list) == 2:
            for x in value_list:
                if (x == '0') or (x == '0.0') or (x == '1') or (x == '1.0'):
                    return ['True', 'False']

        return value_list

    def str_to_bool(self, value_list):
        res = []
        for x in value_list:
            if (x == 'False'):
                res.append(False)
            elif (x == 'True'):
                res.append(True)

        return res if res != [] else value_list


    def cb_filter_value(self, attr, old, new, widget):

        # From General_plot_helper.py
        update_other_selects(old, new, widget, self.filter_widgets, w_type='filters')

        self.edit_button(self.add_filter_button_widget, "Add more filters", "primary")
    
        df = pd.DataFrame(self.plot_data.source_backup.data)
        options=[]
        # if new == 'task':
        #     options = self.plot_data.task_values
        # elif new == 'subspec':
        #     options = self.plot_data.subspec_values
        # elif new != '(select)':
        if new != '(select)':
            options = self.plot_data.get_column_from_name(df, new)
            # Multi-select widget only takes string values as options
            options = [str(x) for x in options]
            options = self.bool_to_str(options)
        
        # From General_plot_helper.py
        widget_index = get_index_from_widget_list(self.filter_widgets, new, w_type="filters")
        if new == '(select)':
            new = ''
        num_of_widgets = len(self.filter_widgets.children[widget_index].children)
        if num_of_widgets == 3:
            self.filter_widgets.children[widget_index].children[1].title = new
            self.filter_widgets.children[widget_index].children[1].options = options
        elif num_of_widgets == 2:
            filter_value_widget = MultiSelect(title=new, value=[], options=options, height=70, width=150, description='Multi Select')
            self.filter_widgets.children[widget_index].children.insert(1, filter_value_widget)
     
    
    def apply_filter(self):
        df = pd.DataFrame(self.plot_data.source_backup.data)

        # print(filter_widgets.children)
        for c in self.filter_widgets.children:
            # print('haha')
            selected_filter = c.children[0].value
            if selected_filter == '(select)':
                continue
            selected_filter_values = c.children[1].value
            
            if selected_filter in self.plot_data.bool_list:  
                # print('hello3?') 
                selected_filter_values = self.str_to_bool(selected_filter_values)
                df = df[df[selected_filter].isin(selected_filter_values)]
            elif selected_filter in self.plot_data.categ_list:
                # print(selected_filter) 
                # print(selected_filter_values)
                # if (selected_filter == 'task') or (selected_filter == 'subspec'):
                #     df = df[df[selected_filter_values].any(axis='columns')]
                # if (str(df[selected_filter][0]).startswith('[')) and (str(df[selected_filter][0]).endswith(']')):
                if df[selected_filter].str.contains('\[').any() and df[selected_filter].str.contains('\]').any():
                    # print('hello4?')
                    # print(str(selected_filter_values))
                    cate_name = list(selected_filter_values)
                    df = df[df[selected_filter].str.contains('|'.join(cate_name), regex=True, na=False)]
                else:    
                    # print('hello2?')      
                    df = df[df[selected_filter].isin(selected_filter_values)]
                # print(np.unique(df[selected_filter].tolist()))
                # print(df)
            else:
                print('Selected filter %s is neither bool nor categorical data, which should not happen' % selected_filter)

        for c in self.range_selectors.children:
            selected_range = c.children[0].children[0].value
            if selected_range == '(select)':
                continue
            selected_range_min = c.children[0].children[1].value
            selected_range_max = c.children[0].children[2].value

            if selected_range in self.numeric_var_ops:
                df = df[df[selected_range].between(selected_range_min, selected_range_max)]
            else:
                print('Selected range %s is not numerical data, which should not happen' % selected_range)

        return df

    def cb_generate(self, selected):
        # The rest are plot specific
        # print(selected)
        # self.plot_data.source.data = selected 
        pass
        

    # Update the range text inputs --- min_widget or max_widget whenever the values in range slider have been changed
    def cb_range_text(self, attr, old, new, slider, widget):
        if widget.title == 'min':
            max_val = slider.value[1]
            slider.value = (new, max_val)
        elif widget.title == 'max':
            min_val = slider.value[0]
            slider.value = (min_val, new)

    # Update the range slider whenever the value in min_widget or max_widget has been changed
    def cb_range(self, attr, old, new, min_widget, max_widget):
        min_widget.value = new[0]
        max_widget.value = new[1]



    def cb_delete(self, w_type, add_button, widget):
        if w_type == 'filters':
            widget_list = self.filter_widgets
        else:
            widget_list = self.range_selectors

        self.edit_button(add_button, "Add more " + w_type, "primary")
        # From General_plot_helper.py
        delete_index = get_index_from_widget_list(widget_list, widget.value, w_type=w_type)
        widget_list.children.remove(widget_list.children[delete_index])
        for c in widget_list.children:
            temp_widget = c.children[0] if w_type == 'filters' else c.children[0].children[0]
            temp_widget.options.append(widget.value)
            temp_widget.options.sort()
    


    def cb_range_select(self, attr, old, new, select, slider, min_widget, max_widget):

        update_other_selects(old, new, select, self.range_selectors, w_type='ranges')

        df = pd.DataFrame(self.plot_data.source_backup.data)
        min_value = df[new].min()
        max_value = df[new].max()
        
        slider.start = min_value
        slider.end = max_value
        slider.value = (min_value, max_value)
        slider.step = (max_value - min_value) // 100
        slider.title = str(new) 

        min_widget.value = min_value
        max_widget.value = max_value
        min_widget.low = min_value
        min_widget.high = max_value
        max_widget.low = min_value
        max_widget.high = max_value       


    def __init__(self, plot_data, layout):
        self.layout = layout
        self.plot_data = plot_data

        # ops - options: meaning the list plus "(select)"
        self.filter_list_ops = self.plot_data.filter_list
        self.filter_list_ops.insert(0, "(select)")

        self.numeric_var_ops = self.plot_data.numeric_var
        self.numeric_var_ops.insert(0, "(select)")

        self.categ_list_ops = self.plot_data.categ_list
        self.categ_list_ops.insert(0, "(select)")





        self.color_select_widget = Select(title='Please select the category for coloring', value="(select)", options=self.categ_list_ops, width=150, height=70, margin=(15, 0, 40, 0))

        # self.upload_text = Div(text='''Please upload your datasheet''')
        # upload_widget = FileInput(accept='.xlsx', width=500, height=40, margin=(0,0,25,0))
        self.add_filter_button_widget = Button(label="Add more filters", button_type="primary", width=150, height=30)

        # The first (categorical and boolean) filter
        self.first_filter_select_widget = Select(title='Please select your filter', value="(select)", options=self.filter_list_ops, width=150, height=70)
        self.first_filter_delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 60, 0))

        self.add_range_button_widget = Button(label="Add more ranges", button_type="primary", width=150, height=30)
        # The first (numerical) range slider
        self.first_range_select_widget = Select(title='Please select your variable', value="(select)", options=self.numeric_var_ops, width=170, height=50)
        self.first_range_widget = RangeSlider(start=0, end=1, value=(0,1), title="", width=370)
        self.first_range_delete_button = Button(label="Delete this range", button_type="primary", width=50, height=30, margin=(15, 0, 0, 0))
        self.first_range_min_widget = NumericInput(value=0, low=0, high=1, title="min")
        self.first_range_max_widget = NumericInput(value=0, low=0, high=1, title="max")

        self.generate_button = Button(label="Generate your plot", button_type="primary",  width=150, height=30, margin=(30, 0, 0, 170))

        self.filter_widgets = column(row(self.first_filter_select_widget, self.first_filter_delete_button))
        self.range_selectors = column(column(row(self.first_range_select_widget, self.first_range_min_widget, self.first_range_max_widget), row(self.first_range_widget, self.first_range_delete_button)))
        self.plot_spec_select_widgets = row()

        
        # self.upload_widget.on_change('value', self.cb_upload)
        
        self.color_select_widget.on_change('value', self.cb_color_select)

        self.first_filter_delete_button.on_click(functools.partial(self.cb_delete, w_type='filters', add_button=self.add_filter_button_widget, widget=self.first_filter_select_widget))
        self.first_filter_select_widget.on_change('value', functools.partial(self.cb_filter_value, widget=self.first_filter_select_widget))

        self.first_range_select_widget.on_change('value', functools.partial(self.cb_range_select, select=self.first_range_select_widget, slider=self.first_range_widget, min_widget=self.first_range_min_widget, max_widget=self.first_range_max_widget))                                            
        self.first_range_widget.on_change('value', functools.partial(self.cb_range, min_widget=self.first_range_min_widget, max_widget=self.first_range_max_widget))
        self.first_range_min_widget.on_change('value', functools.partial(self.cb_range_text, slider=self.first_range_widget, widget=self.first_range_min_widget))
        self.first_range_max_widget.on_change('value', functools.partial(self.cb_range_text, slider=self.first_range_widget, widget=self.first_range_max_widget))
        self.first_range_delete_button.on_click(functools.partial(self.cb_delete, w_type='ranges', add_button=self.add_range_button_widget, widget=self.first_range_select_widget))
        
        self.add_filter_button_widget.on_click(self.cb_add_filter_button)
        self.add_range_button_widget.on_click(self.cb_add_range_button)     
        self.generate_button.on_click(functools.partial(self.cb_generate, self.generate_button))