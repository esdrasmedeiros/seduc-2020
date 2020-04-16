#!/usr/bin/env python
# coding: utf-8

# In[4]:


from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

output_notebook()

import pandas as pd


# In[5]:


df_results = pd.read_csv("results4itemTRI1.txt", sep=" ")
col_names = [  "I14712",   "I15876",  "I15890",  "I24019",  "I26277",  "I27281",  "I28088",  "I28143", 
   "I28578",  "I28637",  "I28646",  "I28904",  "I29167",  "I29359",  "I30755",  "I32149", 
  "I37274",  "I38013",  "I40487",  "I54184",  "I60361",  "I61391",  "I62901",  "I81583", 
  "I82955",  "I83917",  "I8476",   "I10052",  "I16644",  "I17264",  "I24747",  "I25285", 
  "I25723",  "I27005",  "I29844",  "I30029",  "I32686",  "I32969",  "I37515",  "I38786", 
  "I39198",  "I39762",  "I40660",  "I42692",  "I42706",  "I48223",  "I53278",  "I53721", 
  "I59795",  "I60291", "I60315",  "I83234",  "I83608",  "I83906",  "I85018",  "I85050", 
  "I87262",  "I88786",  "I96774",  "I96833",  "I9189",   "I11720",  "I11758",  "I16539", 
  "I17360",  "I17384",  "I23866",  "I29915",  "I30042",  "I40005",  "I40717",  "I43322", 
  "I43940",  "I45300",  "I60235",  "I60584",  "I60724",  "I61485",  "I68172",  "I81410", 
  "I83860",  "I84945",  "I85776",  "I86907",  "I87141",  "I87751",  "I87821",  "I89162", 
  "I89339",  "I95556",  "I95803" , "I96088",  "I96366" , "I96485" , "I5990"  , "I12922" ,
  "I15292",  "I28815" , "I29500" , "I30331",  "I32189" , "I32905" , "I32953" , "I48921", 
  "I53559",  "I61172" , "I62736" , "I66805",  "I82123" , "I82367" , "I83742" , "I84768" ,
  "I86027",  "I97059" , "I98070" , "I111434", "I111487", "I111523", "I111524", "I111535",
  "I111554", "I111557", "I111594", "I111628", "I111692", "I111725"]

df_results.head(10)
    


# In[6]:





source = ColumnDataSource(
        data=dict(
            x=[1, 2, 3, 4, 5],
            y=[2, 5, 8, 2, 7],
            desc=['A', 'b', 'C', 'd', 'E'],
        )
    )

hover = HoverTool(
        tooltips=[
            ("index", "$index"),
            ("(x,y)", "($x, $y)"),
            ("desc", "@desc"),
        ]
    )

p = figure(plot_width=300, plot_height=300, tools=[hover], title="Mouse over the dots")

p.circle('x', 'y', size=20, source=source)

show(p);


# In[7]:


import yaml

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

output_notebook()


# In[8]:


def bkapp(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25),
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource.from_df(data)

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """, Loader=yaml.FullLoader))
    
    


# In[9]:


show(bkapp) # notebook_url="http://localhost:8888"


# In[10]:


import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg_clean as df

df = df.copy()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

# data cleanup
df.cyl = df.cyl.astype(str)
df.yr = df.yr.astype(str)
del df['name']

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

def myapp(doc):
    #set plot
    def create_figure():
        xs = df[x.value].values
        ys = df[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()

        kw = dict()
        if x.value in discrete:
            kw['x_range'] = sorted(set(xs))
        if y.value in discrete:
            kw['y_range'] = sorted(set(ys))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,hover,reset', **kw)
        p.xaxis.axis_label = x_title
        p.yaxis.axis_label = y_title

        if x.value in discrete:
            p.xaxis.major_label_orientation = pd.np.pi / 4

        sz = 9
        if size.value != 'None':
            if len(set(df[size.value])) > N_SIZES:
                groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
            else:
                groups = pd.Categorical(df[size.value])
            sz = [SIZES[xx] for xx in groups.codes]

        c = "#31AADE"
        if color.value != 'None':
            if len(set(df[color.value])) > N_COLORS:
                groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
            else:
                groups = pd.Categorical(df[color.value])
            c = [COLORS[xx] for xx in groups.codes]

        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        
        return p
    
    def update(attr, old, new):
        layout.children[1] = create_figure()
        

    x = Select(title='X-Axis', value='mpg', options=columns)
    x.on_change('value', update)

    y = Select(title='Y-Axis', value='hp', options=columns)
    y.on_change('value', update)

    size = Select(title='Size', value='None', options=['None'] + continuous)
    size.on_change('value', update)

    color = Select(title='Color', value='None', options=['None'] + continuous)
    color.on_change('value', update)

    controls = column(x, y, color, size, width=100)
    layout = row(controls, create_figure())
    doc.add_root(layout)
    doc.title = "Crossfilter"
    #curdoc().add_root(layout)
    #curdoc().title = "Crossfilter"
#     doc.theme = Theme(json=yaml.load("""
#         attrs:            
#             Figure:
#                 background_fill_color: "#2F2F2F"
#                 border_fill_color: "#2F2F2F"
#                 outline_line_color: ""#444444"
#             Axis:
#                 axis_line_color: white
#                 axis_label_text_color: white
#                 major_label_text_color: white
#                 major_tick_line_color: white
#                 minor_tick_line_color: white
#                 minor_tick_line_color: white
#             Grid:
#                 grid_line_dash: [6, 4]
#                 grid_line_alpha: .3
#             Title:
#                 text_color: white
#             """, Loader=yaml.FullLoader))
    
    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """, Loader=yaml.FullLoader))
    
    
    


# In[11]:


df.head(10)


# In[12]:


show(myapp) # notebook_url="http://localhost:8888"


# In[ ]:




