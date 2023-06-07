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

        super(BarChart, self).__init__(plot_data=plot_data, layout=layout)

        self.color_select_widget = Select(title='Please select the category for coloring', value="(select)", options=self.categ_list_ops, width=150, height=70, margin=(15, 0, 40, 0))
        self.color_select_widget.on_change('value', self.cb_color_select)

        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.categ_list_ops, width=245, height=50, margin=(0,0,50,0))
        self.var_1_select_widget.on_change('value', self.cb_var_select)
        
        self.cate_select_widget = MultiSelect(title="Please select categories to plot", value=[], options=[], height=70, width=150, description='Multi Select')

        self.layout.children[0].children.insert(3, self.color_select_widget)
        # Update the plot specific widgets in the super class for further data processing
        self.plot_spec_select_widgets.children.insert(0, self.var_1_select_widget)
        self.plot_spec_select_widgets.children.insert(1, self.cate_select_widget)

    
    # def plot_settings(self, selected, plot_var_1, x_val):
        # x = selected[plot_var_1]

        # self.plot_figure.x_range = FactorRange(factors=x_val)

        # self.plot_figure.x_range.start = x.min()
        # self.plot_figure.x_range.end = x.max()
        # self.plot_figure.y_range.start = y.min()
        # self.plot_figure.y_range.end = y.max()
        # self.plot_figure.xaxis.axis_label = plot_var_1
        # self.plot_figure.yaxis.axis_label = plot_var_2

    # @override
    def cb_upload(self, attr, old, new):
        super().cb_upload(attr, old, new)
        
        for w in self.plot_spec_select_widgets.children:
            w.options = self.plot_data.categ_list
    

    def cb_var_select(self, attr, old, new):
        df = pd.DataFrame(self.plot_data.source_backup.data)
        cate_val = list(self.plot_data.get_column_from_name(df, new))

        self.cate_select_widget.options = cate_val
        self.cate_select_widget.value = cate_val
    
    def cb_color_select(self, attr, old, new):
        self.selected_color_stra = new

    # @override
    def cb_generate(self, button):

        # First delete the plot
        if self.bar != None:
            self.layout.children[1].children.pop(1)
           
        plot_var_1 = str(self.var_1_select_widget.value)

        if (plot_var_1 == "(select)"):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"


            selected = self.apply_filter()
            # print(selected.shape[0])
            # print(selected)
            x_val = self.cate_select_widget.value
            # x_val = selected[plot_var_1]
            # print(selected[plot_var_1].tolist())

            if plot_var_1 in self.plot_data.brackets_list:
                # x_val = self.plot_data.get_column_from_name(selected, plot_var_1)          
                y_val = []
                deleted = []
                for x in x_val:
                    counter = 0
                    for l in selected[plot_var_1].tolist():        
                        if x in str(l):      
                            # if x == 'VGG-F':
                            #     print(str(l))       
                            counter += 1
                    if counter == 0:
                        deleted.append(x)
                    # # TODO delete this
                    # elif counter <= 10:
                    #     deleted.append(x)
                    else:
                        y_val.append(counter)
                
                # print(x_val)
                # print(y_val)
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
                # print(x_val)
                x_val = [x for x in x_val if x not in deleted]
                # print(y_val)
                
                # counting = selected.groupby([plot_var_1]).size()
                # x_val = counting.index.values.tolist()
                # y_val = counting.tolist()

            res = {'x': x_val, 'y': y_val}

            plot_figure = figure(x_range=x_val, height=400, width=500, title='Datasheet visualization', tooltips=None)

            if self.selected_color_stra != '(select)':
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)
                
                if self.selected_color_stra in self.plot_data.brackets_list:
                    # Extract unique data from filter widgets instead of selected because there could be extra values in the bracket lists.     
                    for c in self.filter_widgets.children:
                        if c.children[0].value == self.selected_color_stra:
                            unique_data = c.children[1].value
                
                unique_data.sort()
                
                # unique_data = selected[self.selected_color_stra].unique().tolist()

                if len(unique_data) > 20:
                    button.label = "Too many categories! Please apply filter!"
                    button.button_type = "danger"
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
                        # print(df_stack)
                    else:
                        # If column cell data in form of bracket lists
                        df_stack = pd.DataFrame([])
                        for color in unique_data:
                            stacked_num = []
                            for x in x_val:
                                x_selected = selected.loc[selected[plot_var_1] == x]
                                # print(x_selected)

                                color_selected = x_selected.loc[x_selected[self.selected_color_stra].str.contains('\'' + color + '\'')]
                                # print(color_selected[self.selected_color_stra])

                                stacked_num.append(len(color_selected.index))
                            
                                # print(stacked_num)
                                # print('------------------')
                            df_stack[color] = stacked_num
                        df_stack['x'] = x_val
                        # print(df_stack)
                        # for cat in x_val:
                        #     print(selected.loc[self.selected_color_stra])
                            # count = 0
                            # for color in unique_data:
                            #     if color in selected

                        # for index, row in selected.iterrows():
                            # print(row[])
                            
                        # print(x_val)
                        

                 
                    if len(unique_data) <=2:
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