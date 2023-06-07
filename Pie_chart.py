from bokeh.plotting import figure
from bokeh.models.widgets import Select, MultiSelect
from math import pi
from bokeh.models import LabelSet
from bokeh.transform import cumsum


from General_plot import *
from Plot_Data import *


class PieChart(GeneralPlot):

    pie = None

    def __init__(self, plot_data, layout):

        super(PieChart, self).__init__(plot_data=plot_data, layout=layout)

        self.var_1_select_widget = Select(title="Please select category to plot", value="(select)", options=self.categ_list_ops, width=245, height=50, margin=(0,0,50,0))

        self.var_1_select_widget.on_change('value', self.cb_var_select)
        
        self.cate_select_widget = MultiSelect(title="Please select", value=[], options=[], height=70, width=150, description='Multi Select')

        # Update the plot specific widgets in the super class for further data processing
        self.plot_spec_select_widgets.children.insert(0, self.var_1_select_widget)
        self.plot_spec_select_widgets.children.insert(1, self.cate_select_widget)
    


    def cb_var_select(self, attr, old, new):
        df = pd.DataFrame(self.plot_data.source_backup.data)
        cate_val = list(self.plot_data.get_column_from_name(df, new))

        self.cate_select_widget.options = cate_val
        self.cate_select_widget.value = cate_val
    

    # @override
    def cb_generate(self, button):
        if self.pie != None:
            self.layout.children[1].children.pop(1)
        

        plot_var_1 = str(self.var_1_select_widget.value)

        if (plot_var_1 == "(select)"):
            button.label = "Please re-select variables!"
            button.button_type = "danger"  
        else:
            button.label = "Generate your plot"
            button.button_type = "primary"

            selected = self.apply_filter()

            x_val = self.cate_select_widget.value

            if plot_var_1 in self.plot_data.brackets_list:
                # x_val = self.plot_data.get_column_from_name(selected, plot_var_1)          
                y_val = []
                deleted = []
                for x in x_val:
                    counter = 0
                    for l in selected[plot_var_1]:
                        if x in str(l):
                            counter += 1
                    if counter == 0:
                        deleted.append(x)
                    else:
                        y_val.append(counter)
                
                x_val = [x for x in x_val if x not in deleted]
                    
            else:
                y_val = []
                deleted = []
                for x in x_val:
                    counter = selected[plot_var_1].tolist().count(x)
                    if int(counter) == 0:
                        deleted.append(x)
                    else:
                        y_val.append(counter)
                # print(x_val)
                x_val = [x for x in x_val if x not in deleted]
            
            
            res = pd.DataFrame({'x': x_val, 'y': y_val})

            # values = res['y'].tolist()
            # print(res['y'])
            # print(res['y'].sum())
            if len(x_val) > 20:
                    button.label = "Too many categories! Please apply filter!"
                    button.button_type = "danger"
                    self.pie = None
            else:
                # res['angle'] = [x/sum(values)*2*pi for x in values]
                res['angle'] = res['y'] / res['y'].sum() * 2*pi
                res['percentage'] = res['y'] / res['y'].sum()
                res['color'] = d3['Category20'][len(x_val)]
                # print(res)

            plot_figure = figure(height=400, width=500, title='Datasheet visualization', tooltips=None)

            self.pie = plot_figure.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                                         line_color='white', fill_color='color', legend_field='x', source=res)
            
            print(res['percentage'])
            # res['angle'] = res['angle'].round(2)
            # res['angle'] = ' '.join(str(res['angle']))
            # res['angle'] = (res['angle'] * 100).astype(str) + '%'
            # labels = LabelSet(x=0, y=1, text='angle', angle=cumsum('angle', include_zero=True), source=ColumnDataSource(data=res), text_baseline='top', text_align='center', text_font_size='11px')

            plot_figure.axis.axis_label = None
            plot_figure.axis.visible = False
            plot_figure.grid.grid_line_color = None
            plot_figure.legend.label_text_font_size = '7pt'
            # plot_figure.add_layout(labels)
            
            self.layout.children[1].children.insert(1, plot_figure)