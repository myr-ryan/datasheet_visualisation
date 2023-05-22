from bokeh.io import curdoc
from bokeh.models.widgets import Select
from bokeh.layouts import column, row

from Plot_Data import *
from Scatter_plot import *
from General_plot import *
from Bar_chart import *
import functools




def plot_type_creation(attr, old, new, select_widget):
    select_widget.disabled = True
    # layout = row(column(plot_type_select_widget), column())

    plot = None
    if new == 'scatter':
        plot = ScatterPlot(plot_data)
    elif new == 'bar chart':
        plot = BarChart(plot_data)
    else:
        print('Invalid plot type, please select again.')


    # if len(layout.children[1].children) != 0:       
    #     while len(layout.children[0].children) > 1:
    #         # print('sucess')
    #         layout.children[0].children.pop(1)
    #     layout.children[1].children.clear()
    # print(len(layout.children[1].children))
    
       # print(len(layout.children[0].children))   

    # For General_plot
    # layout.children[0].children.insert(1, plot.upload_text)
    # layout.children[0].children.insert(2, plot.upload_widget)
    layout.children[0].children.insert(3, plot.color_select_widget)
    layout.children[0].children.insert(4, plot.add_filter_button_widget)
    layout.children[0].children.insert(5, plot.filter_widgets)
    layout.children[0].children.insert(6, plot.add_range_button_widget)
    layout.children[0].children.insert(7, plot.range_selectors)
    layout.children[1].children.insert(0, plot.generate_button)

    # Plot specific
    layout.children[0].children.insert(2, plot.plot_spec_select_widgets)
    layout.children[1].children.insert(0, plot.plot_figure)
    
    
    # print(len(layout.children[0].children))
    # plot.upload_widget.on_change('value', plot.cb_upload)
    # plot.generate_button.on_click(functools.partial(plot.update_plot, button=plot.generate_button))

    
 



def cb_upload(attr, old, new):
        
        # Read excel file into dataframe
        decoded = base64.b64decode(new)
        f = io.BytesIO(decoded)
        df = pd.read_excel(f, sheet_name='Sheet1', engine='openpyxl')
        
        plot_data.upload_data(df)
        plot_data.preprocessing()

        # plot_data.debug_printing()
        plot_type_select_widget = Select(title="Please select a plot type", value="(select)", options=['(select)', 'scatter', 'bar chart'], width=245, height=50, margin=(0,0,50,0))
        layout.children[0].children.insert(2, plot_type_select_widget)
        plot_type_select_widget.on_change('value',functools.partial(plot_type_creation, select_widget=plot_type_select_widget))
        

        
empty_data = {'x':[],'y':[]}
plot_data = Plot_Data(empty_data)

upload_widget = FileInput(accept='.xlsx', width=500, height=40, margin=(0,0,25,0))

upload_widget.on_change('value', functools.partial(cb_upload))


layout = row(column(upload_widget), column())
curdoc().add_root(layout)