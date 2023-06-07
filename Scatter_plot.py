from bokeh.models.widgets import Select
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from General_plot import *
from Plot_Data import *

# Widgets and plot settings specially for scatter plot

class ScatterPlot(GeneralPlot):

    selected_color_stra = '(select)'
    scatter = None

    def __init__(self, plot_data, layout):

        
        super(ScatterPlot, self).__init__(plot_data=plot_data, layout=layout)

        self.color_select_widget = Select(title='Please select the category for coloring', value="(select)", options=self.categ_list_ops, width=245, height=70, margin=(15, 0, 40, 0))
        self.color_select_widget.on_change('value', self.cb_color_select)

        # Set up widgets for variables that need to be plotted, and filters to apply
        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.plot_data.numeric_var, width=245, height=50, margin=(0,0,50,0))
        self.var_2_select_widget = Select(title="Please select var on y axis", value="(select)", options=self.plot_data.numeric_var, width=245, height=50, margin=(0,0,50,0))

        # Update the plot specific widgets in the super class for further data processing
        self.layout.children[0].children.insert(3, self.color_select_widget)
        
        self.plot_spec_select_widgets.children.insert(0, self.var_2_select_widget)
        self.plot_spec_select_widgets.children.insert(0, self.var_1_select_widget)


    def plot_settings(self, selected, plot_var_1, plot_var_2, plot_figure):
        # x = selected['x']
        # y = selected['y']
        # plot_figure.x_range.start = x.min()
        # plot_figure.x_range.end = x.max()
        # plot_figure.y_range.start = y.min()
        # plot_figure.y_range.end = y.max()
        plot_figure.xaxis.axis_label = plot_var_1
        plot_figure.yaxis.axis_label = plot_var_2
    


    def cb_color_select(self, attr, old, new):
        self.selected_color_stra = new

        # df = self.plot_data.source_backup.data

        # unique_data = self.plot_data.get_column_from_name(df, self.selected_color_stra)

        # self.color_mul_select_widget.value = unique_data
        # self.color_mul_select_widget.options = unique_data


    # @override
    def cb_generate(self, button):

        # First delete the plot
        if self.scatter != None:
            self.layout.children[1].children.pop(1)

        plot_var_1 = str(self.var_1_select_widget.value)
        plot_var_2 = str(self.var_2_select_widget.value)

        if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"


            selected = self.apply_filter()
                    
            selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})



            # # # Create hover tool
            # hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            # self.plot_figure.add_tools(hover)


            self.plot_data.source.data = selected 


            plot_figure = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
            
            if self.selected_color_stra != '(select)':
 
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)


                if len(unique_data) > 20:
                    print(len(unique_data))
                    button.label = "Too many categories! Please apply filter!"
                    button.button_type = "danger"
                    self.scatter = None
                else:
                    # TODO counting for bracket lists
                    if len(unique_data) <=2:
                        palette = ('#1f77b4', '#ff7f0e')
                    else:
                        palette = d3['Category20'][len(unique_data)]
                    
                    # print(unique_data)
                    index_cmap = factor_cmap(self.selected_color_stra, palette=palette, factors=unique_data)
                    self.scatter = plot_figure.scatter('x', 'y', legend_field=self.selected_color_stra, fill_color=index_cmap, source=selected)
                    # plot_figure.legend.location = "bottom_right"
                    self.plot_settings(selected, plot_var_1, plot_var_2, plot_figure) 
                    self.layout.children[1].children.insert(1, plot_figure)
                    
            else:
                self.scatter = plot_figure.scatter('x', 'y', source=selected)
            
                self.plot_settings(selected, plot_var_1, plot_var_2, plot_figure) 
                self.layout.children[1].children.insert(1, plot_figure)
            
