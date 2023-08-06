#%%
from typing import Optional, Union, Literal, Dict, List
from pydantic import validate_arguments


import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.io as pio

import plotly.express as px

pio.templates["draft"] = go.layout.Template()
pio.templates['draft'].layout.legend = {
    'orientation'   : 'h'
    }
pio.templates['draft'].layout.autosize = False
pio.templates['draft'].layout.width = 1000
pio.templates['draft'].layout.height = 750
pio.templates['draft'].layout.margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    )
plt_colors = px.colors.qualitative.G10
plt_dark_color = 'rgb(102, 102, 102)'
pio.templates['draft'].layout.colorway = plt_colors
pio.templates.default = "plotly_white+draft"
pio.renderers.default='notebook'
#%%


