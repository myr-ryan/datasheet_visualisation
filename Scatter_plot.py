from bokeh.models.widgets import Select
from bokeh.layouts import row
from bokeh.plotting import figure

from General_plot import *
from Plot_Data import *

# Widgets and plot settings specially for scatter plot

class ScatterPlot(GeneralPlot):
    plot_figure = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
    

    def __init__(self, plot_data):
        # empty_data = {'x':[],'y':[]}

        # scatter_plot_data = Plot_Data(empty_data)
        
        self.plot_figure.scatter('x', 'y', source=plot_data.source)

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

            selected = selected[['x', 'y']]
              

            # # Create hover tool
            hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            self.plot_figure.add_tools(hover)
            
            super().cb_generate(selected)
