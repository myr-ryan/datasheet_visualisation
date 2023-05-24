from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.models import FactorRange
from math import pi

from General_plot import *
from Plot_Data import *


class BarChart(GeneralPlot):

    bar = None

    def __init__(self, plot_data, layout):

        super(BarChart, self).__init__(plot_data=plot_data, layout=layout)

        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.plot_data.categ_list, width=245, height=50, margin=(0,0,50,0))

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

        # First clear the data points
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


            counting = selected.groupby([plot_var_1]).size()
            x_val = counting.index.values.tolist()
            y_val = counting.tolist()

            res = {'x': x_val, 'y': y_val}

            plot_figure = figure(x_range=x_val, height=400, width=500, title='Datasheet visualization', tooltips=None)

            if self.selected_color_stra != '(select)':

                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)
                unique_data.sort()
                # print(unique_data)
                # unique_data = selected[self.selected_color_stra].unique().tolist()
                if len(unique_data) > 20:
                    print('Too many categories')
                else: 
                    df_stack = pd.DataFrame([])
                    for cat in x_val:                  
                        stacked_per_task = selected[self.selected_color_stra][selected[plot_var_1] == cat].value_counts(sort=False).to_frame().sort_index()
                        df_stack = pd.concat([df_stack, stacked_per_task], axis=1)

                    df_stack = df_stack.transpose()
                    df_stack.reset_index(inplace=True, drop=True)
                    df_stack = pd.concat([pd.DataFrame(res), df_stack], axis=1)
                    # Bokeh issue, vbar_stack will ignore entire row if first data column is NaN, so need to fill them with 0
                    df_stack = df_stack.fillna(0)

                    palette = d3['Category20'][len(unique_data)]
                    
                    self.bar = plot_figure.vbar_stack(stackers=unique_data, x='x', width=0.5, color=palette, source=df_stack, legend_label=unique_data)
                    
            else:
                self.bar = plot_figure.vbar(x='x', top='y', width=0.5, source=pd.DataFrame(res))
            
                                  
             # Create hover tool
            hover = HoverTool(tooltips=[("Number", "@{y}")])
            plot_figure.add_tools(hover)
            plot_figure.xaxis.major_label_orientation = pi/4

            self.layout.children[1].children.insert(1, plot_figure)