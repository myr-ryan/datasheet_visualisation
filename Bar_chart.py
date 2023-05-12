from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.models import FactorRange

from General_plot import *
from Plot_Data import *


class BarChart(GeneralPlot):
    x_range = FactorRange(factors=[])
    plot_figure = figure(x_range=x_range, height=400, width=500, title='Datasheet visualization', tooltips=None)

    def __init__(self, plot_data):
        # empty_data = {'x':[],'y':[]}

        # barchart_data = Plot_Data(empty_data)
        
        self.plot_figure.vbar(x='x', top='y', width=0.5, source=plot_data.source)

        super(BarChart, self).__init__(plot_data)

        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=[], width=245, height=50, margin=(0,0,50,0))

        # Update the plot specific widgets in the super class for further data processing
        self.plot_spec_select_widgets.children.insert(0, self.var_1_select_widget)

    
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
    

    # @override
    def cb_generate(self, button):
        plot_var_1 = str(self.var_1_select_widget.value)
        # print(plot_var_1)

        if (plot_var_1 == "(select)"):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"

            # selected = pd.DataFrame(scatter_plot_data.source_backup.data)

            selected = super().apply_filter()

            counting = selected.groupby([plot_var_1]).size()
            x_val = counting.index.values.tolist()
            y_val = counting.tolist()

            res = {'x': x_val, 'y': y_val}

            self.plot_figure.x_range.factors = x_val

              

            # # # Create hover tool
            # hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            # self.plot_figure.add_tools(hover)
            
            super().cb_generate(pd.DataFrame(res))