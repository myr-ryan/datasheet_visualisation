


        


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