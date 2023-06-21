from math import pi
from bokeh.models.widgets import MultiSelect
from bokeh.plotting import figure
from bokeh.models import Whisker
from bokeh.transform import factor_cmap


from General_plot import *
from Plot_Data import *


class BoxPlot(GeneralPlot):

    boxplot = None

    def __init__(self, plot_data, layout):

        # Initialize general widgets and call back functions
        super(BoxPlot, self).__init__(plot_data=plot_data, layout=layout)

        self.ops = [x for x in self.plot_data.numeric_var if (('ID' not in x) and ('pmid' not in x) and ('year' not in x))]


        self.var_1_select_widget = MultiSelect(title="Please select", value=self.ops, options=self.ops, height=70, width=150, description='Multi Select')

        self.plot_spec_select_widgets.children[0].children.insert(0, self.var_1_select_widget)

    def plot_settings(self, plot_figure, df):

        plot_figure.y_range.end = df["upper"].max()
        plot_figure.y_range.start = df["lower"].min()
        plot_figure.xgrid.grid_line_color = None
        plot_figure.axis.major_label_text_font_size="14px"
        plot_figure.axis.axis_label_text_font_size="12px"
        # plot_figure.axis.major_label_text_font_size = "7px"
        plot_figure.xaxis.major_label_orientation = pi / 3
        # plot_figure.yaxis.major_label_orientation = pi / 3
 
    # @override
    def cb_generate(self, button):

        # First delete the previous plot
        if self.boxplot != None:
            del self.layout.children[1].children[1]
        
        plot_var_1 = self.var_1_select_widget.value

        if (plot_var_1 == "(select)"):
            # Change button style (function in General_plot_helper file)
            edit_button(button, "Please re-select variables!", "danger")
        else:
            edit_button(button, "Generate your plot", "primary")

            selected = self.apply_filter()

            selected[plot_var_1] = (selected[plot_var_1] - selected[plot_var_1].min(axis=0)) / (selected[plot_var_1].max(axis=0) - selected[plot_var_1].min(axis=0))


            # print(selected[plot_var_1])
            df = pd.DataFrame(selected[plot_var_1].stack(dropna=True), columns=['nums']).reset_index()
            # print(df)


            # # print(plot_var_1)
            qs = df.groupby("level_1").nums.quantile([0.25, 0.5, 0.75])
            # print(qs)
            qs = qs.unstack().reset_index()
            qs.columns = ["level_1", "q1", "q2", "q3"]
            df = pd.merge(df, qs, on="level_1", how="left")
            # print(df)
            # for x in plot_var_1:
                # qs = selected[x].quantile([0.25, 0.5, 0.75])
            # compute IQR outlier bounds
            iqr = df.q3 - df.q1
            df["upper"] = df.q3 + 1.5*iqr
            df["lower"] = df.q1 - 1.5*iqr

            source = ColumnDataSource(df)
            plot_figure = figure(x_range=plot_var_1, height=800, width=500, title='Datasheet visualization', tooltips=None)

            whisker = Whisker(base="level_1", upper="upper", lower="lower", source=source)
            whisker.upper_head.size = whisker.lower_head.size = 20
            plot_figure.add_layout(whisker)

            # quantile boxes
            cmap = factor_cmap("level_1", d3['Category20'][len(plot_var_1)], plot_var_1)
            # cmap = d3['Category20'][len(plot_var_1)]
            plot_figure.vbar("level_1", 0.7, "q2", "q3", source=source, color=cmap, line_color="black")
            plot_figure.vbar("level_1", 0.7, "q1", "q2", source=source, color=cmap, line_color="black")

            # outliers
            outliers = df[~df.nums.between(df.lower, df.upper)]
            plot_figure.scatter("level_1", "nums", source=outliers, size=6, color="black", alpha=0.3)

            self.plot_settings(plot_figure=plot_figure, df=df)

            self.layout.children[1].children.insert(1, plot_figure)
