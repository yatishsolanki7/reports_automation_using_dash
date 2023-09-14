from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import io
import base64
import pandas as pd

import plotly.express as px
import datetime
from app import app
from app import df

layout = html.Div([
    html.H1('Country-wise Sales and Customer data', style={"textAlign": "center"}),
    html.H1('', style={"textAlign": "center"}),
    html.H3('Filter data on basis of Date, Country names and Stock lists from below filters', style={"textAlign": "left"}),
    html.Div(["Select date range :- ", dcc.DatePickerRange(id='dt_range_p1',
                                                               min_date_allowed=datetime.date(df.InvoiceDate.min().year,
                                                                                              df.InvoiceDate.min().month,
                                                                                              df.InvoiceDate.min().day),
                                                               max_date_allowed=datetime.date(df.InvoiceDate.max().year,
                                                                                              df.InvoiceDate.max().month,
                                                                                              df.InvoiceDate.max().day),
                                                               initial_visible_month=datetime.date(df.InvoiceDate.min().year,
                                                                                                   df.InvoiceDate.min().month,
                                                                                                   df.InvoiceDate.min().day)
                                                               )
              ]),
    html.H1('', style={"textAlign": "center"}),
    html.Div(
        className="row", children=[
            html.Div(className='country dropdown p1', children=[
                dcc.Dropdown(
                    id='country_dropdown_p1', clearable=False,
                    options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in
                                                                                sorted(df.Country.unique())],
                    multi=True, placeholder="Select countries from here"
                )
            ], style=dict(width='20%'))
            , html.Div(className='stockcd dropdown p1', children=[
                dcc.Dropdown(
                    id='stock_cd_dropdown_p1', clearable=False,
                    options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in
                                                                                sorted(df.StockCode.unique())],
                    multi=True, placeholder="Select stock lists from here"
                )
            ], style=dict(width='20%'))
        ],
        style=dict(display='flex')

    ),

    html.H1('', style={"textAlign": "center"}),

    html.A(
        'Download Report',
        id='rep-download',
        download="report.xlsx",
        href="",
        target="_blank"),

    dcc.Graph(id='sales_dist_p1', figure={})
])


@app.callback(
    Output('rep-download', 'href'),
    [Input(component_id='dt_range_p1', component_property='start_date'),
     Input(component_id='dt_range_p1', component_property='end_date'),
     Input(component_id='country_dropdown_p1', component_property='value'),
     Input(component_id='stock_cd_dropdown_p1', component_property='value')]
)

def display_value(st_dt, end_dt, country_chosen, stock_cd_chosen):
    if st_dt is None:
        raise PreventUpdate
    elif end_dt is None:
        raise PreventUpdate
    elif country_chosen is None:
        raise PreventUpdate
    elif stock_cd_chosen is None:
        raise PreventUpdate
    else:

        dfv_fltrd = df[df['InvoiceDate'] >= st_dt]
        dfv_fltrd = dfv_fltrd[dfv_fltrd['InvoiceDate'] <= end_dt]
        if 'all_values' in country_chosen:
            dfv_fltrd = dfv_fltrd
        else:
            dfv_fltrd = dfv_fltrd[dfv_fltrd['Country'].isin(country_chosen)]
        if "all_values" in stock_cd_chosen:
            dfv_fltrd = dfv_fltrd
        else:
             dfv_fltrd = dfv_fltrd[dfv_fltrd['StockCode'].isin(stock_cd_chosen)]

        dfv_fltrd['sales'] = dfv_fltrd['Quantity'] * dfv_fltrd['UnitPrice']

        mis = dfv_fltrd.groupby([dfv_fltrd.InvoiceDate.dt.year, dfv_fltrd.InvoiceDate.dt.month]).agg({'InvoiceNo': lambda x: x.nunique(),
                                                                                 'CustomerID': lambda x: x.nunique(),
                                                                                 'sales': 'sum', 'Quantity': 'sum'})

        mis.index.set_names(['Year', 'Month'], inplace=True)
        mis.rename(columns={'InvoiceNo': '# Orders', 'CustomerID': '# Customers',
                            'sales': 'Gross Sales', 'Quantity':'Units Sold'}, inplace=True)
        mis = mis.transpose()

        sales_dist = dfv_fltrd.groupby(['Country Name', 'iso_alpha']).agg({'sales': lambda x: x.sum(),
                                                                           'CustomerID':lambda x:x.nunique()}).reset_index()
        sales_dist = sales_dist.sort_values(['sales'], ascending=False)
        sales_dist = sales_dist.rename(columns = {'sales':'Total Sales', 'CustomerID':'# Customers'})

        xlsx_io = io.BytesIO()
        writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
        mis.to_excel(writer, sheet_name='MIS')
        sales_dist.to_excel(writer, sheet_name='Country_wise_dist')
        writer.save()
        xlsx_io.seek(0)
        # https://en.wikipedia.org/wiki/Data_URI_scheme
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        href_data_downloadable = f'data:{media_type};base64,{data}'
        return href_data_downloadable


@app.callback(
    Output(component_id='sales_dist_p1', component_property='figure'),
    [Input(component_id='dt_range_p1', component_property='start_date'),
     Input(component_id='dt_range_p1', component_property='end_date'),
     Input(component_id='country_dropdown_p1', component_property='value'),
     Input(component_id='stock_cd_dropdown_p1', component_property='value')]
)




def display_value(st_dt, end_dt, country_chosen, stock_cd_chosen):
    if st_dt is None:
        raise PreventUpdate
    elif end_dt is None:
        raise PreventUpdate
    elif country_chosen is None:
        raise PreventUpdate
    elif stock_cd_chosen is None:
        raise PreventUpdate
    else:

        dfv_fltrd = df[df['InvoiceDate'] >= st_dt]
        dfv_fltrd = dfv_fltrd[dfv_fltrd['InvoiceDate'] <= end_dt]
        if 'all_values' in country_chosen:
            dfv_fltrd = dfv_fltrd
        else:
            dfv_fltrd = dfv_fltrd[dfv_fltrd['Country'].isin(country_chosen)]
        if "all_values" in stock_cd_chosen:
            dfv_fltrd = dfv_fltrd
        else:
             dfv_fltrd = dfv_fltrd[dfv_fltrd['StockCode'].isin(stock_cd_chosen)]

        dfv_fltrd['sales'] = dfv_fltrd['Quantity'] * dfv_fltrd['UnitPrice']
        sales_dist = dfv_fltrd.groupby(['Country Name', 'iso_alpha']).agg({'sales': lambda x: x.sum(),
                                                                           'CustomerID':lambda x:x.nunique()}).reset_index()
        sales_dist = sales_dist.sort_values(['sales'], ascending=False)
        sales_dist = sales_dist.rename(columns = {'sales':'Total Sales', 'CustomerID':'# Customers'})

        fig1 = px.choropleth(sales_dist, locations="iso_alpha",
                            color="# Customers",  # sales is a column of gapminder
                            hover_name="Country Name",  # column to add to hover information
                            hover_data=["# Customers", "Total Sales"],
                            color_continuous_scale=px.colors.sequential.Plasma)

        return fig1


