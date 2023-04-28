from bokeh.models.widgets import Select
from bokeh.layouts import row
from bokeh.plotting import figure

from General_plot import *
from Plot_Data import *

# Widgets and plot settings specially for scatter plot

class ScatterPlot(GeneralPlot):
    plot_spec_select_widget_list = []
    plot_figure = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)
    # First create an empty plot
    


    def __init__(self):
        empty_data = {'x':[],'y':[]}

        scatter_plot_data = Plot_Data(empty_data)
        
        self.plot_figure.scatter('x', 'y', source=scatter_plot_data.source)

        super(ScatterPlot, self).__init__(scatter_plot_data)
        # Set up widgets for variables that need to be plotted, and filters to apply
        var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=[], width=245, height=50, margin=(0,0,50,0))
        var_2_select_widget = Select(title="Please select var on y axis", value="(select)", options=[], width=245, height=50, margin=(0,0,50,0))
        self.plot_spec_select_widget_list.append(var_1_select_widget)
        self.plot_spec_select_widget_list.append(var_2_select_widget)

        # Update the plot specific widgets in the super class for further data processing
        # super().plot_spec_select_widgets = row(var_1_select_widget, var_2_select_widget)
        super().plot_spec_select_widgets.children += self.plot_spec_select_widget_list



        # print(self.plot_spec_select_widgets)

    # Callback for button_apply
    def update_plot(self, button):
        # print(len(self.plot_spec_select_widgets.children))
        plot_var_1 = str(self.var_1_select_widget.value)
        plot_var_2 = str(self.var_2_select_widget.value)

        if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"

            # selected = pd.DataFrame(scatter_plot_data.source_backup.data)

            selected = super().apply_filter(selected)

            
            # plot_settings(plot, selected, plot_var_1, plot_var_2)

            # selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})
            # scatter_plot_data.source.data = selected    

            # # Create hover tool
            # hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            # plot.add_tools(hover)

    def plot_settings(plot, selected, plot_var_1, plot_var_2):
        x = selected[plot_var_1]
        y = selected[plot_var_2]
        plot.x_range.start = x.min()
        plot.x_range.end = x.max()
        plot.y_range.start = y.min()
        plot.y_range.end = y.max()
        plot.xaxis.axis_label = plot_var_1
        plot.yaxis.axis_label = plot_var_2