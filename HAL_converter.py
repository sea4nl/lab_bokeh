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
read_every_n = 10
n_rows = 84078
skip = np.arange(n_rows)
skip = np.delete(skip, np.arange(0, n_rows, read_every_n))
for s in HAL_list:
    df = pd.read_csv("HAL"+"/"+s, sep="\t", index_col=0, parse_dates=False, skiprows=skip)
    df.to_csv("HAL_small"+"/"+s, sep="\t")

