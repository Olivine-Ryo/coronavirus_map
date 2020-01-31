import numpy as np
import pandas as pd

import json

from IPython.display import HTML
import colorlover as cl
from plotly.subplots import make_subplots
import plotly.express as px

from IPython.display import HTML
import colorlover as cl
from plotly.subplots import make_subplots
import plotly.express as px

from plotly import offline

import os

import copy
import math

import plotly_express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


dfs = []
for l in os.listdir("./csv/"):
    if ".csv" in l:
        dfs.append(pd.read_csv("./csv/" +l))
df = pd.concat(dfs, sort=False).reset_index(drop=True)
df["Last Update"] = pd.to_datetime(df["Last Update"])
df.Confirmed = df.Confirmed.fillna(0).astype("int")
df.Suspected = df.Suspected.fillna(0).fillna(0).astype("int")
df.Deaths = df.Deaths.fillna(0).fillna(0).astype("int")
df.Recovered = df.Recovered.fillna(0).astype("int")
df["日付"] = df["Last Update"].apply(lambda x: str(x.year) + "-" + str(x.month) + "-" + str(x.day))
df = df.sort_values("Last Update")


df_global = copy.deepcopy(df.drop("Province/State",axis=1))

df_global[['Confirmed', 'Suspected', 'Recovered', 'Deaths']] = df[["日付",'Country/Region', 'Confirmed', 'Suspected', 'Recovered', 'Deaths']].groupby(["日付","Country/Region"]).transform(sum)

df_global = df_global[~df_global.duplicated(["Country/Region","Last Update"])].reset_index(drop=True)

country_cd = pd.read_csv("./geo_data/country_cd.csv")
df_global = pd.merge(df_global,country_cd[["Country/Region","alpha3"]], on="Country/Region", how="left")
df_global = df_global.rename({"alpha3": "国コード"},axis=1)

key = "Confirmed"

zrange=max(abs(df_global[key].max()),abs(df_global[key].min()))
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
    df_global_plot = df_global[df_global["日付"] == timestamp_input]
    fig = px.choropleth(df_global_plot, locations="国コード",
                        color="Confirmed", # lifeExp is a column of gapminder
                        hover_name="Country/Region", # column to add to hover information
                        color_continuous_scale="PuRd",
                        projection="natural earth",
                        range_color=(zmin,zmax))
    fig.update_layout(
        title="新型コロナウイルス感染者数(国別)")

    return fig


app.run_server(debug=True)