import numpy as np
import pandas as pd
import json
import os
import copy
import math

from IPython.display import HTML
import colorlover as cl

from plotly.subplots import make_subplots
import plotly.express as px
from plotly import offline

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


dfs = []
for l in os.listdir("./csv_ja/"):
    if ".csv" in l:
        dfs.append(pd.read_csv("./csv_ja/" +l))
df_japan = pd.concat(dfs, sort=False).reset_index(drop=True)
df_japan["Last Update"] = pd.to_datetime(df_japan["Last Update"])
df_japan["日付"] = df_japan["Last Update"].apply(lambda x: str(x.year) + "-" + str(x.month) + "-" + str(x.day))
df_japan = df_japan.sort_values("Last Update")

with open("./geo_data/jp_prefs.geojson") as f:
    geojson_japan = json.load(f)

key = "Confirmed"
#cmap = cl.scales['10']['div']
    
zrange=df_japan[key].max()
zmax = zrange #df2[key].max()
zmin = 0 #df2[key].min()

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
        dcc.Input(id ='date' ,value='2020-1-25'),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(Output("graph", "figure"), [Input('date', 'value')])
def make_figure(timestamp_input):
    #print(df_global["日付"].unique())
    df_japan_plot = df_japan[df_japan["日付"] == timestamp_input]
    fig = px.choropleth(df_japan_plot,
                        geojson = geojson_japan,
                        featureidkey="properties.NAME_JP",
                        locations="Province/State",
                        color=key, # lifeExp is a column of gapminder
                        hover_name="Province/State", # column to add to hover information
                        color_continuous_scale="PuRd",
                        projection="mercator",
                        range_color=(zmin,zmax),
                        width=600, height=800)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title="新型コロナウイルス感染者数(都道府県)")

    return fig

if __name__=='__main__':
    app.run_server(debug=True)