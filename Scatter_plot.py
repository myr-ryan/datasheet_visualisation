from bokeh.models.widgets import Select
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import factor_cmap


from General_plot import *
from Plot_Data import *

# Widgets and plot settings specially for scatter plot

class ScatterPlot(GeneralPlot):
    plot_figure = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
    

    def __init__(self, plot_data):
        # empty_data = {'x':[],'y':[]}

        # scatter_plot_data = Plot_Data(empty_data)
        
        

        super(ScatterPlot, self).__init__(plot_data)
        # Set up widgets for variables that need to be plotted, and filters to apply
        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.plot_data.numeric_var, width=245, height=50, margin=(0,0,50,0))
        self.var_2_select_widget = Select(title="Please select var on y axis", value="(select)", options=self.plot_data.numeric_var, width=245, height=50, margin=(0,0,50,0))

        # Update the plot specific widgets in the super class for further data processing
        
        self.plot_spec_select_widgets.children.insert(0, self.var_2_select_widget)
        self.plot_spec_select_widgets.children.insert(0, self.var_1_select_widget)


    def plot_settings(self, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        self.plot_figure.x_range.start = x.min()
        self.plot_figure.x_range.end = x.max()
        self.plot_figure.y_range.start = y.min()
        self.plot_figure.y_range.end = y.max()
        self.plot_figure.xaxis.axis_label = plot_var_1
        self.plot_figure.yaxis.axis_label = plot_var_2
    

    # # @override
    # def cb_upload(self, attr, old, new):
    #     super().cb_upload(attr, old, new)
        
    #     for w in self.plot_spec_select_widgets.children:
    #         w.options = self.plot_data.numeric_var

    # @override
    def cb_generate(self, button):
        # print(len(self.plot_spec_select_widgets.children))
        plot_var_1 = str(self.var_1_select_widget.value)
        plot_var_2 = str(self.var_2_select_widget.value)
        # print(plot_var_1)
        # print(plot_var_2)

        if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"

            # selected = pd.DataFrame(scatter_plot_data.source_backup.data)

            selected = super().apply_filter()
            
            

            
            
            self.plot_settings(selected, plot_var_1, plot_var_2)

            selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})

            # selected = selected[['x', 'y']]

            # # Create hover tool
            hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            self.plot_figure.add_tools(hover)


            # print(self.selected_color_stra)
            # super().cb_generate(selected)
            self.plot_data.source.data = selected 

            # print(self.selected_color_stra)
            if self.selected_color_stra != '(select)':
                if (self.selected_color_stra == 'task') or (self.selected_color_stra == 'subspec'):
                    # Make task or subspec columns categorical data, and attached to the selected dataframe, 
                    # note that there could be multiple tasks or subspecs in a single paper. So left join was used
                    list_name = self.selected_color_stra + '_values'
                    # print(list_name)
                    cols_to_cat = selected.loc[:, getattr(self.plot_data, list_name)]
                    cols_to_cat = pd.DataFrame({self.selected_color_stra: cols_to_cat.columns[np.where(cols_to_cat)[1]]}, np.where(cols_to_cat)[0])

                    # left join by default
                    selected = cols_to_cat.join(selected)
                else:
                    pass
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)
                # print(unique_data)
                # unique_data = selected[self.selected_color_stra].unique().tolist()
                if len(unique_data) > 20:
                    print('Too many categories')
                else:
                    palette = d3['Category20'][len(unique_data)]
                    # self.scatter.glyph.fill_color = palette
                    # color_map = CategoricalColorMapper(factors=unique_data, palette=palette)
                    index_cmap = factor_cmap(self.selected_color_stra, palette=palette, factors=unique_data)
                    # # self.scatter.fill_color = palette
                    # print(selected)
                    # print(self.selected_color_stra)
                    # 
                    self.plot_figure.reset_policy = 'event_only'
                    # TODO no reset
                    self.plot_figure.reset.emit()

                    self.scatter = self.plot_figure.scatter('x', 'y', legend_field=self.selected_color_stra, fill_color=index_cmap, source=selected)
                    # self.scatter.glyph.fill_color = {'field': self.selected_color_stra, 'transform': color_map}
            else:
                self.scatter = self.plot_figure.scatter('x', 'y', source=selected)
            
