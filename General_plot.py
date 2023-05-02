from bokeh.models.widgets import Select, FileInput, Button, RangeSlider, MultiSelect, NumericInput
from bokeh.models import Div, HoverTool
import base64
import io
import pandas as pd
import functools
from bokeh.layouts import column, row

# Widgets and plot settings for all plots

class GeneralPlot:
    upload_text = Div(text='''Please upload your datasheet''')
    upload_widget = FileInput(accept='.xlsx', width=500, height=40, margin=(0,0,25,0))
    add_filter_button_widget = Button(label="Add more filters", button_type="primary", width=150, height=30)

    # The first (categorical and boolean) filter
    first_filter_select_widget = Select(title='Please select your filter', value="(select)", options=[], width=150, height=70)
    first_delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 60, 0))

    add_range_button_widget = Button(label="Add more ranges", button_type="primary", width=150, height=30)
    # The first (numerical) range slider
    first_range_select_widget = Select(title='Please select your variable', value="(select)", options=[], width=170, height=50)
    first_range_widget = RangeSlider(start=0, end=1, value=(0,1), title="", width=370)
    first_range_delete_button = Button(label="Delete this range", button_type="primary", width=50, height=30, margin=(15, 0, 0, 0))
    first_range_min_widget = NumericInput(value=0, low=0, high=1, title="min")
    first_range_max_widget = NumericInput(value=0, low=0, high=1, title="max")

    generate_button = Button(label="Generate your plot", button_type="primary",  width=150, height=30, margin=(30, 0, 0, 5))

    filter_widgets = column(row(first_filter_select_widget, first_delete_button))
    range_selectors = column(column(row(first_range_select_widget, first_range_min_widget, first_range_max_widget), row(first_range_widget, first_range_delete_button)))
    plot_spec_select_widgets = row()


    def get_index_from_widget_list(self, widget_value):
        # print(filter_widgets.children)
        index = -1
        for i in range(len(self.filter_widgets.children)):
            if self.filter_widgets.children[i].children[0].value == widget_value:
                return i
        print('Failed to find in the widget list')
        return index

    def upload_data(self, attr, old, new):
        # Read excel file into dataframe
        decoded = base64.b64decode(new)
        f = io.BytesIO(decoded)
        df = pd.read_excel(f, sheet_name='Sheet1_before_combining', engine='openpyxl')

        self.plot_data.upload_data(df)
        self.plot_data.preprocessing()

        for w in self.plot_spec_select_widgets.children:
            w.options = self.plot_data.numeric_var
        
        # Update the first filter widget
        self.first_filter_select_widget.options = self.plot_data.filter_list

        # Update the first range slider
        self.first_range_select_widget.options = self.plot_data.numeric_var
    
    def edit_button(self, button, label, type):
        button.label = label
        button.button_type = type


    def delete_widget_and_button(self, widget):
        self.edit_button(self.add_filter_button_widget, "Add more filters", "primary")
        delete_index = self.get_index_from_widget_list(widget.value)
        # print(filter_widgets.children[delete_index].children)
        # print(delete_index)
        self.filter_widgets.children.remove(self.filter_widgets.children[delete_index])
        for c in self.filter_widgets.children:
            c.children[0].options.append(widget.value)
            c.children[0].options.sort()


    def add_more_filters(self):

        total_options = self.plot_data.filter_list
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
                delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 0, 0))


                new_filter_widget.on_change('value', functools.partial(self.add_filter_value, widget=new_filter_widget))
                delete_button.on_click(functools.partial(self.delete_widget_and_button, widget=new_filter_widget))

                # Insert a row, where the first element is the filter widget, the second element will be the value widget
                self.filter_widgets.children.insert(0, row(new_filter_widget, delete_button))

    def add_more_ranges(self):

        total_options = self.plot_data.numeric_var
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
                # TODO Need to remove options in other selectable variables
                new_range_select_widget = Select(title='Please select your variable', value="(select)", options=options, width=170, height=50)
                new_range_widget = RangeSlider(start=0, end=1, value=(0,1), title="", width=370)
                new_range_delete_button = Button(label="Delete this range", button_type="primary", width=50, height=30, margin=(15, 0, 0, 0))
                new_range_min_widget = NumericInput(value=0, low=0, high=1, title="min")
                new_range_max_widget = NumericInput(value=0, low=0, high=1, title="max")

              
                new_range_select_widget.on_change('value', functools.partial(self.upload_range_data, slider=new_range_widget, min_widget=new_range_min_widget, max_widget=new_range_max_widget))                                                     
                new_range_widget.on_change('value', functools.partial(self.update_range_text, min_widget=new_range_min_widget, max_widget=new_range_max_widget))
                new_range_min_widget.on_change('value', functools.partial(self.update_range_slider, slider=new_range_widget, widget=new_range_min_widget))
                new_range_max_widget.on_change('value', functools.partial(self.update_range_slider, slider=new_range_widget, widget=new_range_max_widget))

                # new_filter_widget = Select(title='Please select your filter', value='(select)', options=options, width=150, height=70)
                # delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 0, 0))


                # new_filter_widget.on_change('value', functools.partial(self.add_filter_value, widget=new_filter_widget))
                # delete_button.on_click(functools.partial(self.delete_widget_and_button, widget=new_filter_widget))

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


    def add_filter_value(self, attr, old, new, widget):

        # If the filter is selected from scretch, remove the '(select)' option
        if old == '(select)':
            widget.options.remove('(select)')
        # If the selected filter changed, need to update other filter's options as well      
        for c in self.filter_widgets.children:
            if c.children[0] != widget:
                c.children[0].options.remove(new)
                if old != '(select)':
                    c.children[0].options.append(old)
                c.children[0].options.sort()

        self.edit_button(self.add_filter_button_widget, "Add more filters", "primary")
    
        df = pd.DataFrame(self.plot_data.source_backup.data)
        options=[]
        if new == 'tasks':
            options = self.plot_data.task_values
        elif new == 'subspec':
            options = self.plot_data.subspec_values
        elif new != '(select)':
            options = self.plot_data.get_column_from_name(df, new)
            # Multi-select widget only takes string values as options
            options = [str(x) for x in options]
            options = self.bool_to_str(options)
        
        widget_index = self.get_index_from_widget_list(new)
        if new == '(select)':
            new = ''
        num_of_widgets = len(self.filter_widgets.children[widget_index].children)
        if num_of_widgets == 3:
            self.filter_widgets.children[widget_index].children[1].title = new
            self.filter_widgets.children[widget_index].children[1].options = options
        elif num_of_widgets == 2:
            filter_value_widget = MultiSelect(title=new, value=[], options=options, height=70, width=150, description='Multi Select')
            self.filter_widgets.children[widget_index].children.insert(1, filter_value_widget)
     
        
    

    # TODO apply range slider filter
    def apply_filter(self):
        df = pd.DataFrame(self.plot_data.source_backup.data)

        # print(filter_widgets.children)
        for c in self.filter_widgets.children:
            selected_filter = c.children[0].value
            if selected_filter == '(select)':
                continue
            selected_filter_values = c.children[1].value
            
            if selected_filter in self.plot_data.bool_list:
                if (selected_filter == 'tasks') or (selected_filter == 'subspec'):
                    df = df[df[selected_filter_values].any(axis='columns')]
                else:
                    selected_filter_values = self.str_to_bool(selected_filter_values)
                    df = df[df[selected_filter].isin(selected_filter_values)]
            elif selected_filter in self.plot_data.categ_list:
                df = df[df[selected_filter].isin(selected_filter_values)]
            else:
                print('Selected filter %s is neither bool nor categorical data, which should not happen', selected_filter)

        return df

    def update_plot(self, selected):
        # The rest are plot specific
        self.plot_data.source.data = selected  

    # Update the range text inputs --- min_widget or max_widget whenever the values in range slider have been changed
    def update_range_slider(self, attr, old, new, slider, widget):
        if widget.title == 'min':
            max_val = slider.value[1]
            slider.value = (new, max_val)
        elif widget.title == 'max':
            min_val = slider.value[0]
            slider.value = (min_val, new)

    # Update the range slider whenever the value in min_widget or max_widget has been changed
    def update_range_text(self, attr, old, new, min_widget, max_widget):
        min_widget.value = new[0]
        max_widget.value = new[1]


    def upload_range_data(self, attr, old, new, slider, min_widget, max_widget):
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


    def __init__(self, plot_data):
        self.plot_data = plot_data
        self.upload_widget.on_change('value', self.upload_data)

        self.first_delete_button.on_click(functools.partial(self.delete_widget_and_button, widget=self.first_filter_select_widget))
        self.first_filter_select_widget.on_change('value', functools.partial(self.add_filter_value, widget=self.first_filter_select_widget))
              
        self.first_range_select_widget.on_change('value', functools.partial(self.upload_range_data, slider=self.first_range_widget, min_widget=self.first_range_min_widget, max_widget=self.first_range_max_widget))
                                                 
        self.first_range_widget.on_change('value', functools.partial(self.update_range_text, min_widget=self.first_range_min_widget, max_widget=self.first_range_max_widget))
        self.first_range_min_widget.on_change('value', functools.partial(self.update_range_slider, slider=self.first_range_widget, widget=self.first_range_min_widget))
        self.first_range_max_widget.on_change('value', functools.partial(self.update_range_slider, slider=self.first_range_widget, widget=self.first_range_max_widget))
        # TODO delete range button on_click

        self.add_filter_button_widget.on_click(self.add_more_filters)
        self.add_range_button_widget.on_click(self.add_more_ranges)
        # Create a button widget for filters
        
        # 
        self.generate_button.on_click(self.update_plot)

