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

        # Initialize general widgets and call back functions
        super(ScatterPlot, self).__init__(plot_data=plot_data, layout=layout)

        # For scatter plot, user need to select x and y axis variable
        self.var_1_select_widget = Select(title="Please select var on x axis", value="(select)", options=self.numeric_var_ops, width=245, height=50, margin=(0,0,50,0))
        self.var_2_select_widget = Select(title="Please select var on y axis", value="(select)", options=self.numeric_var_ops, width=245, height=50, margin=(0,0,50,0))

        # For scatter plot, user could select colors for stratefication
        self.color_select_widget = Select(title='Please select the category for coloring', value="(select)", options=self.categ_list_ops, width=245, height=70, margin=(15, 0, 40, 0))
        self.color_select_widget.on_change('value', self.cb_color_select)
        
        # Update the plot specific widgets in the super class for further data processing        
        self.plot_spec_select_widgets.children[0].children.insert(0, self.var_2_select_widget)
        self.plot_spec_select_widgets.children[0].children.insert(0, self.var_1_select_widget)
        self.plot_spec_select_widgets.children.insert(1, row(self.color_select_widget))


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

    
    # @override
    def cb_generate(self, button):

        # First delete the previous plot
        if self.scatter != None:
            del self.layout.children[1].children[1]

        plot_var_1 = str(self.var_1_select_widget.value)
        plot_var_2 = str(self.var_2_select_widget.value)

        if (plot_var_1 == "(select)") or (plot_var_2 == "(select)") or (plot_var_1 == plot_var_2):
            # Change button style (function in General_plot_helper file)
            edit_button(button, "Please re-select variables!", "danger")
        else:
            edit_button(button, "Generate your plot", "primary")

            # First apply filters (function in General_plot file)
            selected = self.apply_filter()
            
            # Create x and y columns for plotting
            selected['x'] = selected[plot_var_1]
            selected['y'] = selected[plot_var_2]
            # selected = selected.rename(columns={plot_var_1: 'x', plot_var_2: 'y'})

            self.plot_data.source.data = selected 

   
            plot_figure = figure(height=400, width=500, title= plot_var_1 + ' versus ' + plot_var_2, tooltips=None)

            # Next deal with coloring if there is any
            if self.selected_color_stra != '(select)':
 
                unique_data = self.plot_data.get_column_from_name(selected, self.selected_color_stra)

                # If dealing with brackets_list data and if the category for coloring is being filtered, extract only selected values.
                if self.selected_color_stra in self.plot_data.brackets_list:
                    # Extract unique data from filter widgets instead of selected because there could be extra values in the bracket lists.     
                    for c in self.filter_widgets.children:
                        if c.children[0].value == self.selected_color_stra:
                            unique_data = c.children[1].value
                

                if len(unique_data) > 20:
                    edit_button(button, "Too many categories! Please apply filter!", "danger")
                    self.scatter = None
                else:
                    # Bokeh color palette only work for > 3, deal with 1 and 2 manualy      
                    if len(unique_data) == 1:   
                        palette = ('#1f77b4')
                    elif len(unique_data) == 2:
                        palette = ('#1f77b4', '#ff7f0e')
                    else:
                        palette = d3['Category20'][len(unique_data)]

                    if self.selected_color_stra not in self.plot_data.brackets_list:
           
                        # print(unique_data)
                        index_cmap = factor_cmap(self.selected_color_stra, palette=palette, factors=unique_data)
                        self.scatter = plot_figure.scatter('x', 'y', legend_field=self.selected_color_stra, fill_color=index_cmap, source=selected)
                        # plot_figure.legend.location = "bottom_right"
                        self.plot_settings(selected, plot_var_1, plot_var_2, plot_figure) 
                        self.layout.children[1].children.insert(1, plot_figure)
                    
                    # Deal with brackets_list data separately
                    # Need to separate every value in brackets_list -> increase the row numbers
                    else:
                        # Leave the original columns, create a new one (will delete this column later)
                        # Remove []
                        selected[self.selected_color_stra + '_temp'] = selected[self.selected_color_stra].map(lambda x: x.lstrip('[').rstrip(']'))
                        # Split the values in brackets into different rows
                        temp = selected[self.selected_color_stra + '_temp'].str.split(', ').apply(pd.Series, 1).stack()
                        temp.index = temp.index.droplevel(-1)
                        new_column_name = self.selected_color_stra + '_new'
                        temp.name = new_column_name
                        del selected[self.selected_color_stra + '_temp']
                        selected = selected.join(temp)
                        # Remove ''
                        selected[new_column_name] = selected[new_column_name].map(lambda x: x.lstrip('\'').rstrip('\''))
                        selected = selected.loc[selected[new_column_name].isin(unique_data)]


                        index_cmap = factor_cmap(new_column_name, palette=palette, factors=unique_data)
                        self.scatter = plot_figure.scatter('x', 'y', legend_field=new_column_name, fill_color=index_cmap, source=selected)
                        # plot_figure.legend.location = "bottom_right"
                        self.plot_settings(selected, plot_var_1, plot_var_2, plot_figure) 
                        self.layout.children[1].children.insert(1, plot_figure)
                        # print(selected[new_column_name])
                        hover = HoverTool(tooltips=[(plot_var_2, "@{y}"), (plot_var_1, "@{x}"), (self.selected_color_stra, "@{" + new_column_name + "}")])
                        plot_figure.add_tools(hover)


                        
            else:
                self.scatter = plot_figure.scatter('x', 'y', source=selected)
            
                self.plot_settings(selected, plot_var_1, plot_var_2, plot_figure) 
                self.layout.children[1].children.insert(1, plot_figure)
            
