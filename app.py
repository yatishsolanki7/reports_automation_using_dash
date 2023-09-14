# gethroughapp = {
#     'User': 'User@123!'
# }
import pathlib
import pandas as pd
import datetime
import dash
import plotly.express as px
# import dash_bootstrap_components as dbc

# import dash_auth

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("transactional_data.csv"))
df['InvoiceDate'] = df['InvoiceDate'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

# country mapping
df['Country Name'] = df['Country']
df['Country Name'] = df['Country Name'].replace({'RSA':'South Africa', 'EIRE':'Ireland','USA' : 'United States'})
df1 = px.data.gapminder().query("year==2007")
df1['Country Name'] = df1['country']
df = pd.merge(df, df1[['Country Name', 'iso_alpha']], how='left', on='Country Name')

del df1

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True,
#                 meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
# , external_stylesheets=[dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# auth = dash_auth.BasicAuth(
#     app,
#     gethroughapp
# )

server = app.server



