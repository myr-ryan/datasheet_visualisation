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
        
        # self.vbar = self.plot_figure.vbar(x='x', top='y', width=0.5, source=plot_data.source)
        # self.vbar = self.plot_figure.vbar_stack(stackers=[], x='x', width=0.5, source=plot_data.source)

        super(BarChart, self).__init__(plot_data)

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
            print(selected.shape[0])

            if plot_var_1 == 'task':
                x_val = self.plot_data.task_values
                y_val = [selected[c].sum() for c in x_val]
            elif plot_var_1 == 'subspec':
                x_val = self.plot_data.subspec_values
                y_val = [selected[c].sum() for c in x_val]
            else:
                counting = selected.groupby([plot_var_1]).size()
                x_val = counting.index.values.tolist()
                y_val = counting.tolist()

            res = {'x': x_val, 'y': y_val}
            # print(x_val)
            # print(y_val)

            # # Add the results to the final dataframe
            # selected['x'] = x_val
            # selected['y'] = y_val
            self.plot_figure.x_range.factors = x_val

              

            # # # Create hover tool
            # hover = HoverTool(tooltips=[("Paper ID", "@{Paper ID}")])
            # self.plot_figure.add_tools(hover)
            # print(self.vbar)
            # self.vbar.stackers = plot_var_1

            # super().cb_generate(pd.DataFrame(res))

            if self.selected_color_stra != '(select)':
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)
                # print(unique_data)
                # unique_data = selected[self.selected_color_stra].unique().tolist()
                if len(unique_data) > 20:
                    print('Too many categories')
                else:
                    # df_stack = selected[[plot_var_1, self.selected_color_stra]]
                    # print(df_stack)
                    # count = df_stack[self.selected_color_stra].unique().size
                    df_stack = pd.DataFrame([])
                    for cat in x_val:
                        # print(df_stack[self.selected_color_stra][df_stack[plot_var_1] == cat].value_counts())
                        # print(selected[self.selected_color_stra][selected[plot_var_1] == cat].value_counts())
                        # print(type(selected[self.selected_color_stra][selected[plot_var_1] == cat].value_counts(sort=False)))
                        df_stack = pd.concat([df_stack, selected[self.selected_color_stra][selected[plot_var_1] == cat].value_counts(sort=False).to_frame()], axis=1)

                    df_stack = df_stack.transpose()
                    df_stack.reset_index(inplace=True, drop=True)
                    # print(pd.DataFrame(res))
                    # print(df_stack)
                    df_stack = pd.concat([pd.DataFrame(res), df_stack], axis=1)
                    # print(df_stack)



                    palette = d3['Category20'][len(unique_data)]
                    # self.scatter.glyph.fill_color = palette
                    # color_map = CategoricalColorMapper(factors=unique_data, palette=palette)
                    # # self.scatter.fill_color = palette
                    self.plot_figure.vbar_stack(stackers=unique_data, x='x', width=0.5, color=palette, source=df_stack, legend_label=unique_data)
                    
                    # self.vbar.glyph.fill_color = {'field': self.selected_color_stra, 'transform': color_map}
            else:
                self.plot_figure.vbar(x='x', top='y', width=0.5, source=pd.DataFrame(res))