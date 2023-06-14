from math import pi
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.transform import linear_cmap
from bokeh.models import BasicTicker, PrintfTickFormatter

from scipy.stats import skew

from General_plot import *
from Plot_Data import *



class HeatMap(GeneralPlot):

    heatmap = None

    def extract(self, num_list):
        pass
    
    def __init__(self, plot_data, layout):

        # Initialize general widgets and call back functions
        super(HeatMap, self).__init__(plot_data=plot_data, layout=layout)

        self.ops = [x for x in self.plot_data.numeric_var if 'ID' in x or 'pmid' in x]

        self.ops.insert(0, '(select)')

        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.ops, width=245, height=50, margin=(0,0,50,0))

        self.plot_spec_select_widgets.children[0].children.insert(0, self.var_1_select_widget)


    def plot_settings(self, plot_figure):
        plot_figure.grid.grid_line_color = None
        plot_figure.axis.axis_line_color = None
        plot_figure.axis.major_tick_line_color = None
        plot_figure.axis.major_label_text_font_size = "7px"
        plot_figure.axis.major_label_standoff = 0
        plot_figure.xaxis.major_label_orientation = pi / 3
        # plot_figure.yaxis.major_label_orientation = pi / 3
        
    
    # @override
    def cb_generate(self, button):

        # First delete the previous plot
        if self.heatmap != None:
            del self.layout.children[1].children[1]

        plot_var_1 = self.var_1_select_widget.value

        if (plot_var_1 == "(select)"):
            # Change button style (function in General_plot_helper file)
            edit_button(button, "Please re-select variables!", "danger")
        else:
            edit_button(button, "Generate your plot", "primary")

            selected = self.apply_filter()
            # print(selected.iloc[:, 0:3])

            # selected = selected.iloc[0:10, :]
            # print(selected)

            selected[plot_var_1] = selected[plot_var_1].astype(str)


            all_plotable = [x for x in self.plot_data.numeric_var if x not in self.ops]
            all_plotable = [x for x in all_plotable if x != 'year']

            selected[all_plotable] = selected[all_plotable].fillna(0)
            # print(all_plotable)

            # Min-max normalization -> scale to 0-1
            # print(selected['performance_mean'])

            # for ap in all_plotable:
            #     print(selected[ap])
            #     print(selected[ap] - selected[ap].min()) / (selected[ap].max() - selected[ap].min())
            #     selected[ap] = (selected[ap] - selected[ap].min()) / (selected[ap].max() - selected[ap].min())
                # print(selected[ap])

            # Robust data scaling -> (value - median) / IQR, where IQR = p75 - p25
            quantiles = selected[all_plotable].quantile([0.0, 0.25, 0.5, 0.75, 1.0], axis=0)
            
            # for ap in all_plotable:
                # Calculate the skewness
                # print(ap)
                # print(quantiles.loc[0.0, ap])
                # print(quantiles.loc[0.25, ap])
                # print(quantiles.loc[0.75, ap])
                # print(quantiles.loc[1.0, ap])

                # print(selected[ap])
                
                # skewness = skew(selected[ap], axis=0)
                # if skewness > 0:
                #     selected[ap] = (selected[ap] - selected[ap].median(axis=0)) / (quantiles.loc[0.5, ap] - quantiles.loc[0.0, ap])
                # elif skewness < 0:
                #     selected[ap] = (selected[ap] - selected[ap].median(axis=0)) / (quantiles.loc[1.0, ap] - quantiles.loc[0.5, ap])
                # else:
                #     selected[ap] = (selected[ap] - selected[ap].median(axis=0)) / (quantiles.loc[0.75, ap] - quantiles.loc[0.25, ap])
                # print(selected[ap])
                # print(selected[ap].max())
                # print(selected[ap].min())
                # break


       
            # # print(quantiles)
            # for ap in all_plotable:
            #     if (quantiles.loc[0.75, ap] - quantiles.loc[0.25, ap]) != 0:
            #         selected[ap] = (selected[ap] - selected[ap].median(axis=0)) / (quantiles.loc[0.75, ap] - quantiles.loc[0.25, ])
            # else:
            
            # Min-max normalization
            selected[all_plotable] = (selected[all_plotable] - selected[all_plotable].min(axis=0)) / (selected[all_plotable].max(axis=0) - selected[all_plotable].min(axis=0))


            
            # print(selected['patient_num'])

            # print(selected['performance_NPV'])

            # import matplotlib.pyplot as plt
            # plt.hist(selected['DataSize_all'].tolist())
            # plt.show()

            # all_plotable = ['performance_auc', 'performance_precision (PPV)', 'performance_specificity', 'performance_NPV', 'performance_sensitivity (recall)', 'performance_F1', 'performance_accuracy', 'performance_mean']

            # all_plotable = ['DataSize_all', 'DataSize_validation', 'DataSize_testing', 'DataSize_training']

            # selected[all_plotable].columns.name = 'all_num'

            df = pd.DataFrame(selected[all_plotable].stack(dropna=False), columns=['nums']).reset_index()
    
            df = df.join(selected, on='level_0')
            # print(df)

            # Bokeh only accept str type as categorical factors
            # df[plot_var_1] = df[plot_var_1].astype(str)

            # x_range = selected[plot_var_1].tolist()
            x_range = list(selected.index)
            x_range = [str(x) for x in x_range]

            
            plot_figure = figure(height=1500, width=500, title='Heatmap', 
                                 x_range=all_plotable, y_range=x_range,
                                 x_axis_location='above', 
                                 tooltips=None)
            
            self.plot_settings(plot_figure=plot_figure)
            
            

            # colors = d3['Category20'][20]
            colors = ["#f7fcf0", "#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081"]




            self.heatmap = plot_figure.rect(x='level_1', y='level_0', width=1, height=1, source=df,
                                 fill_color=linear_cmap('nums', colors, low=df.nums.min(), high=df.nums.max()),
                                 line_color=None)
            
            plot_figure.add_layout(self.heatmap.construct_color_bar(major_label_text_font_size="7px", 
                                  ticker=BasicTicker(desired_num_ticks=len(colors)), 
                                  formatter=PrintfTickFormatter(format="%d"),
                                  label_standoff=6,
                                  border_line_color=None,
                                  padding=5), 'right')

            # plot_figure.rect(x=plot_var_1, y='all_num')
            

            self.layout.children[1].children.insert(1, plot_figure)