from math import pi
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.transform import linear_cmap
from bokeh.models import BasicTicker, PrintfTickFormatter

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

            # selected = selected.iloc[0:20, :]
            # print(selected)

            selected[plot_var_1] = selected[plot_var_1].astype(str)

            all_plotable = [x for x in self.plot_data.numeric_var if x not in self.ops]

            # all_plotable = ['performance_auc', 'performance_precision (PPV)', 'performance_specificity', 'performance_NPV', 'performance_sensitivity (recall)', 'performance_F1', 'performance_accuracy', 'performance_mean']

            all_plotable = ['DataSize_all', 'DataSize_validation', 'DataSize_testing', 'DataSize_training']

            # selected[all_plotable].columns.name = 'all_num'

            df = pd.DataFrame(selected[all_plotable].stack(dropna=False), columns=['nums']).reset_index()
    
            df = df.join(selected, on='level_0')

            # Bokeh only accept str type as categorical factors
            # df[plot_var_1] = df[plot_var_1].astype(str)

            # x_range = selected[plot_var_1].tolist()
            x_range = list(selected.index)
            x_range = [str(x) for x in x_range]

            df['nums'] = df['nums'].fillna(0)
            # print(df)

            # print(df[plot_var_1])
            # print(df['level_1'])
            # print(df['nums'])
            # print(df['nums'])
            
            
            plot_figure = figure(height=400, width=500, title='Heatmap', 
                                 x_range=x_range, y_range=all_plotable,
                                 x_axis_location='above', 
                                 tooltips=None)
            
            plot_figure.grid.grid_line_color = None
            plot_figure.axis.axis_line_color = None
            plot_figure.axis.major_tick_line_color = None
            plot_figure.axis.major_label_text_font_size = "7px"
            plot_figure.axis.major_label_standoff = 0
            plot_figure.xaxis.major_label_orientation = pi / 3
            plot_figure.yaxis.major_label_orientation = pi / 3
            
            colors = d3['Category20'][20]
            # colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
            # fill_color = linear_cmap('nums', colors, low=df.nums.min(), high=df.nums.max())
            # print(fill_color)


            self.heatmap = plot_figure.rect(x='level_0', y='level_1', width=1, height=1, source=df,
                                 fill_color=linear_cmap('nums', colors, low=df.nums.min(), high=df.nums.max()),
                                 line_color=None)
            
            plot_figure.add_layout(self.heatmap.construct_color_bar(major_label_text_font_size="7px", 
                                  ticker=BasicTicker(desired_num_ticks=len(colors)), 
                                  formatter=PrintfTickFormatter(format="%d"),
                                  label_standoff=6,
                                  border_line_color=None,
                                  padding=5), 'right')

            plot_figure.rect(x=plot_var_1, y='all_num')
            

            self.layout.children[1].children.insert(1, plot_figure)