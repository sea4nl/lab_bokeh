from bokeh.io import curdoc, show
from bokeh.layouts import column, row, grid
from bokeh.models import LinearAxis, Range1d, HoverTool, ColumnDataSource, DataTable, Select, CustomJS
from bokeh.models.widgets import TextInput, Button, Paragraph, MultiSelect, MultiChoice
from bokeh.plotting import figure

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from datetime import datetime

HAL_list = listdir("HAL")
HAL_list.sort()
HAL_dict = {}
for i in range(len(HAL_list)):
    key = HAL_list[i].replace("HAL.tsv.","")
    key = key.replace("-", " ")
    #date = datetime.strptime(key, "%Y %m %d")
    HAL_dict[key] = HAL_list[i]

sel_list = list(HAL_dict.keys())
enum_sel = [ ( str(ii), str(f)) for ii, f in enumerate(sel_list) ]
sel = [ list(HAL_dict.keys())[-1] ]
reactor = "1"
react = int(reactor)
read_every_n = 100
n_rows = 84078
skip = np.arange(n_rows)
skip = np.delete(skip, np.arange(0, n_rows, read_every_n))
df = pd.read_csv("HAL"+"/"+HAL_dict[sel[0]], sep="\t", index_col=0, parse_dates=False, skiprows=skip)
source = ColumnDataSource(data=dict(
    x = pd.to_datetime(df.index, dayfirst=True),
    do = df.iloc[:,(react - 1)].values,
    ph = df.iloc[:,(react + 7)].values,
    acid = df.iloc[:,(14 + react * 2)].values,
    base = df.iloc[:,(15 + react * 2)].values
))

# create some widgets
select = MultiSelect(title="Date:", value=sel, options=list(HAL_dict.keys()), height=300)
select.js_on_change("value", CustomJS(code="""
    console.log('select: value=' + this.value, this.toString())
"""))
select2 = Select(title="Reactor:", value=reactor, options=['1','2','3','4','5','6','7','8'])
select3 = TextInput(title="Read every Nth line:", value=str(read_every_n))
button = Button(label="Look up")
#multi_choice = MultiChoice(value=[sel_list[-1]], options=sel_list)


p = figure(x_axis_type='datetime')
p.extra_y_ranges={}
p.extra_y_ranges['do'] = Range1d(start = 0, end = 100)
p.extra_y_ranges['pH'] = Range1d(start = 0, end = 14)
p.add_layout(LinearAxis(y_range_name='pH', axis_label='pH'), 'right')
p.line('x', 'do', source=source, legend_label='do', line_width=2, color="blue", alpha=0.5)
p.line('x', 'ph', source=source, legend_label='pH', line_width=2, color="red", alpha=0.5, y_range_name='pH')
p.add_tools(HoverTool(tooltips=[('date', '@x{%F %T}'),('do','@do'),('pH', '@ph')],
          formatters={'@x': 'datetime'}))

p2 = figure(x_axis_type='datetime', x_range = p.x_range)
base = source.data['base']
p2.extra_y_ranges = {"base": Range1d(start=base.min(), end=base.max())}
p2.add_layout(LinearAxis(y_range_name="base"), 'right')
p2.line('x', 'acid', source=source, legend_label='acid', line_width=2, color="red", alpha=0.5)
p2.line('x', 'base', source=source, legend_label='base', line_width=2, color="blue", alpha=0.5, y_range_name='base')
p2.add_tools(HoverTool(tooltips=[('date', '@x{%F %T}'),('Acid','@acid'),('Base', '@base')],
          formatters={'@x': 'datetime'}))

p3 = figure(x_axis_type='datetime')
p3.line('x', 'base', source=source, legend_label='base', line_width=2, color="blue", alpha=0.5)
p3.add_tools(HoverTool(tooltips=[('date', '@x{%F %T}'),('Base','@base')],
          formatters={'@x': 'datetime'}))

data_table = DataTable(source=source)
output = Paragraph()

def update():
    selection = select.value
    tsv_selected = [HAL_dict[ii] for ii in selection]
    react = int(select2.value)
    read_every_n = int(select3.value)
    n_rows = 84078
    skip = np.arange(n_rows)
    skip = np.delete(skip, np.arange(0, n_rows, read_every_n))
    colnames = [ str(i) for i in range(1,39)]
    df = pd.concat((pd.read_csv("HAL"+"/"+f, sep="\t", index_col=0, parse_dates=False, skiprows = skip, names=colnames) for f in tsv_selected))
    print(select.value)
    print(react)
    source.data = dict(
        x = pd.to_datetime(df.index, dayfirst=True),
        do = df.iloc[:,(react - 1)].values,
        ph = df.iloc[:,(react + 7)].values,
        acid = df.iloc[:,(14 + react * 2)].values,
        base = df.iloc[:,(15 + react * 2)].values
    )
    base = source.data['base']
    acid = source.data['acid']
    p2.y_range.start = acid.min()
    p2.y_range.end = acid.max()
    p2.extra_y_ranges['base'].start = base.min()
    p2.extra_y_ranges['base'].end = base.max()

    xx = source.data['x']
    p.x_range.start = xx.min()
    p.x_range.end = xx.max()

# add a callback to a widget
button.on_click(update)

# update one

# create a layout for everything
controls = column(select, select2, select3, button, width=200)
#plots = column(p, row(p2, p3, sizing_mode="stretch_both"), sizing_mode="stretch_both")
plots = column(p, p2, sizing_mode="stretch_both")

layout = grid([
    [controls, plots]
])

# add the layout to curdoc
curdoc().add_root(layout)