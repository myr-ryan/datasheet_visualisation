from bokeh.models.widgets import Select, Button, RangeSlider, NumericInput
from bokeh.models import Div, HoverTool
from bokeh.layouts import column, row


# def create_new_ones():
#     # upload_text = Div(text='''Please upload your datasheet''')
#     # upload_widget = FileInput(accept='.xlsx', width=500, height=40, margin=(0,0,25,0))
#     # add_filter_button_widget = Button(label="Add more filters", button_type="primary", width=150, height=30)

#     # The first (categorical and boolean) filter
#     first_filter_select_widget = Select(title='Please select your filter', value="(select)", options=[], width=150, height=70)
#     first_filter_delete_button = Button(label="Delete this filter", button_type="primary", width=50, height=30, margin=(40, 0, 60, 0))

#     # add_range_button_widget = Button(label="Add more ranges", button_type="primary", width=150, height=30)
#     # The first (numerical) range slider
#     first_range_select_widget = Select(title='Please select your variable', value="(select)", options=[], width=170, height=50)
#     first_range_widget = RangeSlider(start=0, end=1, value=(0,1), title="", width=370)
#     first_range_delete_button = Button(label="Delete this range", button_type="primary", width=50, height=30, margin=(15, 0, 0, 0))
#     first_range_min_widget = NumericInput(value=0, low=0, high=1, title="min")
#     first_range_max_widget = NumericInput(value=0, low=0, high=1, title="max")

#     # generate_button = Button(label="Generate your plot", button_type="primary",  width=150, height=30, margin=(30, 0, 0, 170))

#     filter_widgets = column(row(first_filter_select_widget, first_filter_delete_button))
#     range_selectors = column(column(row(first_range_select_widget, first_range_min_widget, first_range_max_widget), row(first_range_widget, first_range_delete_button)))
#     plot_spec_select_widgets = row()

#     return filter_widgets, range_selectors, plot_spec_select_widgets
     





def update_other_selects(old, new, select_widget, widget_list, w_type):
    # If the filter is selected from scretch, remove the '(select)' option
    if old == '(select)':
        select_widget.options.remove('(select)')
    # If the selected filter changed, need to update other filter's options as well      
    for c in widget_list.children:
        temp_widget = c.children[0] if w_type == 'filters' else c.children[0].children[0]
        if temp_widget != select_widget:
            temp_widget.options.remove(new)
            if old != '(select)':
                temp_widget.options.append(old)
            temp_widget.options.sort()
    


def get_index_from_widget_list(widget_list, widget_value, w_type):
        index = -1
        for i in range(len(widget_list.children)):
            temp_w_value = widget_list.children[i].children[0].value if w_type == 'filters' else widget_list.children[i].children[0].children[0].value
            if temp_w_value == widget_value:
                return i
        print('Failed to find in the widget list')
        return index

def edit_button(button, label, type):
    button.label = label
    button.button_type = type


