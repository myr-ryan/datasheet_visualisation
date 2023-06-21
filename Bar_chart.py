from bokeh.plotting import figure
from bokeh.models.widgets import Select, MultiSelect
from bokeh.models import FactorRange, LabelSet
from math import pi

from General_plot import *
from Plot_Data import *


class BarChart(GeneralPlot):

    selected_color_stra = '(select)'
    bar = None

    def __init__(self, plot_data, layout):

        # Initialize general widgets and call back functions
        super(BarChart, self).__init__(plot_data=plot_data, layout=layout)

        # For bar chart, user only need to select x axis variable
        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.categ_list_ops, width=245, height=50, margin=(0,0,50,0))
        self.var_1_select_widget.on_change('value', self.cb_var_select)
        self.cate_select_widget = MultiSelect(title="Please select categories to plot", value=[], options=[], height=70, width=150, description='Multi Select')

        # For bar chart, user could select colors for stratefication
        self.color_select_widget = Select(title='Please select the category for coloring', value="(select)", options=self.categ_list_ops, width=150, height=70, margin=(15, 0, 40, 0))
        self.color_select_widget.on_change('value', self.cb_color_select)        
           
        # Update the plot specific widgets in the super class for further data processing
        self.plot_spec_select_widgets.children[0].children.insert(0, self.var_1_select_widget)
        self.plot_spec_select_widgets.children[0].children.insert(1, self.cate_select_widget)
        self.plot_spec_select_widgets.children.insert(1, row(self.color_select_widget))


    
    # def plot_settings(self, selected, plot_var_1, x_val):
        # x = selected[plot_var_1]

        # self.plot_figure.x_range = FactorRange(factors=x_val)

        # self.plot_figure.x_range.start = x.min()
        # self.plot_figure.x_range.end = x.max()
        # self.plot_figure.y_range.start = y.min()
        # self.plot_figure.y_range.end = y.max()
        # self.plot_figure.xaxis.axis_label = plot_var_1
        # self.plot_figure.yaxis.axis_label = plot_var_2


    def cb_var_select(self, attr, old, new):
        # After selecting x axis variable, the multi-select widget need to be updated
        df = pd.DataFrame(self.plot_data.source_backup.data)
        cate_val = list(self.plot_data.get_column_from_name(df, new))
        self.cate_select_widget.options = cate_val
        self.cate_select_widget.value = cate_val
    
    def cb_color_select(self, attr, old, new):
        self.selected_color_stra = new

    # @override
    def cb_generate(self, button):

        # First delete the previous plot
        if self.bar != None:
            del self.layout.children[1].children[1]
        
        plot_var_1 = str(self.var_1_select_widget.value)

        if (plot_var_1 == "(select)"):
            # Change button style (function in General_plot_helper file)
            edit_button(button, "Please re-select variables!", "danger")
        else:
            edit_button(button, "Generate your plot", "primary")

            # First apply filters (function in General_plot file)
            selected = self.apply_filter()
            # Extract x axis from the multi-select widget
            x_val = self.cate_select_widget.value

            # Next count the frequency for each x axis value
            # brackets_list could contain multiple values, so need to deal with it separately
            if plot_var_1 in self.plot_data.brackets_list:
                y_val = []
                deleted = []
                for x in x_val:
                    counter = 0
                    for l in selected[plot_var_1].tolist():
                        # Adding '\'' + .. + '\'' is to prevent scenarios like DenseNet will also be detected in DenseNet121        
                        if '\'' + x + '\'' in str(l):           
                            counter += 1
                    if counter == 0:
                        deleted.append(x)
                    # # TODO delete this
                    # elif counter <= 10:
                    #     deleted.append(x)
                    else:
                        y_val.append(counter)
                
                x_val = [x for x in x_val if x not in deleted]
                    
            else:
                y_val = []
                deleted = []
                for x in x_val:
                    counter = selected[plot_var_1].tolist().count(x)
                    if int(counter) == 0:
                        deleted.append(x)
                    else:
                        y_val.append(counter)
                
                x_val = [x for x in x_val if x not in deleted]

            top_20_string = ''
            if len(x_val) > 20:
                top_20_idx = np.argsort(y_val)[-20:].tolist()
                # print(top_20_idx)
                x_val = [x_val[x] for x in top_20_idx]
                y_val = [y_val[y] for y in top_20_idx]
                top_20_string += '(top20)'
            else:
                sorted_idx = np.argsort(y_val).tolist()
                x_val = [x_val[x] for x in sorted_idx]
                y_val = [y_val[y] for y in sorted_idx]

            # Result for plotting
            res = {'x': x_val, 'y': y_val}

            plot_figure = figure(x_range=x_val, height=400, width=500, title= plot_var_1 + ' distribution' + top_20_string, tooltips=None)

            # Next deal with coloring if there is any
            if self.selected_color_stra != '(select)':
                # Extract all categories that could be colored from dataframe 'selected'
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)
                
                # If dealing with brackets_list data and if the category for coloring is being filtered, extract only selected values.
                if self.selected_color_stra in self.plot_data.brackets_list:
                    # Extract unique data from filter widgets instead of selected because there could be extra values in the bracket lists.     
                    for c in self.filter_widgets.children:
                        if c.children[0].value == self.selected_color_stra:
                            unique_data = c.children[1].value
                
                unique_data.sort()
                
                if len(unique_data) < 20:
                    edit_button(button, "Too many categories! Please apply filter!", "danger")
                    self.bar = None     
                else:     

                    if self.selected_color_stra not in self.plot_data.brackets_list:
                        df_stack = pd.DataFrame([])
                        for cat in x_val:                  
                            stacked_per_task = selected[self.selected_color_stra][selected[plot_var_1] == cat].value_counts(sort=False).to_frame().sort_index()
                            df_stack = pd.concat([df_stack, stacked_per_task], axis=1)

                        df_stack = df_stack.transpose()
                        df_stack.reset_index(inplace=True, drop=True)
                        df_stack = pd.concat([pd.DataFrame(res), df_stack], axis=1)
                        # Bokeh: vbar_stack will ignore entire row if first data column is NaN, so need to fill them with 0
                        df_stack = df_stack.fillna(0)     

                    # Deal with brackets_list data separately
                    else:
                        df_stack = pd.DataFrame([])
                        for color in unique_data:
                            stacked_num = []
                            for x in x_val:
                                x_selected = selected.loc[selected[plot_var_1] == x]

                                color_selected = x_selected.loc[x_selected[self.selected_color_stra].str.contains('\'' + color + '\'')]

                                stacked_num.append(len(color_selected.index))
                            
                            df_stack[color] = stacked_num
                        
                        df_stack['y'] = df_stack.sum(axis=1)
                        df_stack['x'] = x_val
                        # print(df_stack)
                    
                        
                    # Bokeh color palette only work for > 3, deal with 1 and 2 manualy      
                    if len(unique_data) == 1:   
                        palette = ('#1f77b4')
                    elif len(unique_data) == 2:
                        palette = ('#1f77b4', '#ff7f0e')
                    else:
                        palette = d3['Category20'][len(unique_data)]
                    
                    
                    self.bar = plot_figure.vbar_stack(stackers=unique_data, x='x', width=0.5, color=palette, source=df_stack, legend_label=unique_data)
                    labels = LabelSet(x='x', y='y', text='y', x_offset=5, y_offset=5, source=ColumnDataSource(data=df_stack), text_align='right', text_font_size='11px')
                    # Create hover tool
                    hover = HoverTool(tooltips=[("Number", "@{y}")])
                    plot_figure.add_tools(hover)
                    plot_figure.xaxis.major_label_orientation = pi/4
                    plot_figure.add_layout(labels)
                    self.layout.children[1].children.insert(1, plot_figure)
            
            else:
                self.bar = plot_figure.vbar(x='x', top='y', width=0.5, source=pd.DataFrame(res))
                labels = LabelSet(x='x', y='y', text='y', x_offset=5, y_offset=5, source=ColumnDataSource(data=res), text_align='right', text_font_size='11px')
                          
                # Create hover tool
                hover = HoverTool(tooltips=[("Number", "@{y}")])
                plot_figure.add_tools(hover)
                plot_figure.xaxis.major_label_orientation = pi/4
                plot_figure.add_layout(labels)
                self.layout.children[1].children.insert(1, plot_figure)