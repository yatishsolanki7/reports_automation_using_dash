from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.express as px
import datetime
from app import app
from app import df

layout = html.Div([
    html.H1('Top/Bottom 10 Stocks by Sales and Customers', style={"textAlign": "center"}),
    html.H1('', style={"textAlign": "center"}),
    html.H3('Filter data on basis of Date, Country names and Stock lists from below filters', style={"textAlign": "left"}),

    html.Div(["Select date range :- ", dcc.DatePickerRange(id='dt_range_p2',
                                                          min_date_allowed= datetime.date(df.InvoiceDate.min().year,
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
            html.Div(className='country dropdown p2', children=[
                dcc.Dropdown(
                    id='country_dropdown_p2', clearable=False,
                    options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in
                                                                                sorted(df.Country.unique())],
                    multi=True, placeholder="Select countries from here"
                )
            ], style=dict(width='20%'))
            , html.Div(className='stockcd dropdown p2', children=[
                dcc.Dropdown(
                    id='stock_cd_dropdown_p2', clearable=False,
                    options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in
                                                                                sorted(df.StockCode.unique())],
                    multi=True, placeholder="Select stock lists from here"
                )
            ], style=dict(width='20%'))
        ],
        style=dict(display='flex')

    ),
    html.H1('', style={"textAlign": "center"}),
    dcc.Graph(id='sales_top_p2', figure={}),
    html.H1('', style={"textAlign": "center"}),
    dcc.Graph(id='sales_bottom_p2', figure={}),
    html.H1('', style={"textAlign": "center"}),
    dcc.Graph(id='cust_top_p2', figure={}),
    html.H1('', style={"textAlign": "center"}),
    dcc.Graph(id='cust_bottom_p2', figure={})

])


@app.callback(
    Output(component_id='sales_top_p2', component_property='figure'),
    [Input(component_id='dt_range_p2', component_property='start_date'),
     Input(component_id='dt_range_p2', component_property='end_date'),
     Input(component_id='country_dropdown_p2', component_property='value'),
     Input(component_id='stock_cd_dropdown_p2', component_property='value')]
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

        dfv_fltrd['sales'] = dfv_fltrd['Quantity']* dfv_fltrd['UnitPrice']
        sales_dist = dfv_fltrd.groupby(['Description']).agg({'sales': lambda x: x.sum()}).reset_index()
        sales_dist = sales_dist.sort_values(['sales'], ascending=False)
        sales_dist = sales_dist[:10]
        fig1 = px.bar(sales_dist, x='Description', y="sales")
        fig1 = fig1.update_yaxes(tickprefix="$")
        fig1.update_layout(
            title="Top 10 Stocks by Sales",
            xaxis_title="Stocks Description",
            yaxis_title="Sales")
        return fig1

#
@app.callback(
    Output(component_id='sales_bottom_p2', component_property='figure'),
    [Input(component_id='dt_range_p2', component_property='start_date'),
     Input(component_id='dt_range_p2', component_property='end_date'),
     Input(component_id='country_dropdown_p2', component_property='value'),
     Input(component_id='stock_cd_dropdown_p2', component_property='value')]
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

        dfv_fltrd['sales'] = dfv_fltrd['Quantity']* dfv_fltrd['UnitPrice']
        sales_dist = dfv_fltrd.groupby(['Description']).agg({'sales': lambda x: x.sum()}).reset_index()
        sales_dist = sales_dist.sort_values(['sales'], ascending=True)
        sales_dist = sales_dist[:10]
        fig2 = px.bar(sales_dist, x='Description', y="sales")
        fig2 = fig2.update_yaxes(tickprefix="$")
        fig2.update_layout(
            title="Bottom 10 Stocks by Sales",
            xaxis_title="Stocks Description",
            yaxis_title="Sales")
        return fig2


@app.callback(
    Output(component_id='cust_top_p2', component_property='figure'),
    [Input(component_id='dt_range_p2', component_property='start_date'),
     Input(component_id='dt_range_p2', component_property='end_date'),
     Input(component_id='country_dropdown_p2', component_property='value'),
     Input(component_id='stock_cd_dropdown_p2', component_property='value')],

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

        cust_dist = dfv_fltrd.groupby(['Description']).agg({'CustomerID':lambda x:x.nunique()}).reset_index()
        cust_dist = cust_dist.sort_values(['CustomerID'], ascending=False)
        cust_dist = cust_dist[:10]
        fig3 = px.bar(cust_dist, x='Description', y="CustomerID")
        fig3.update_layout(
            title="Top 10 Stocks by Customer Count",
            xaxis_title="Stocks Description",
            yaxis_title="# Customers")
        return fig3



@app.callback(
    Output(component_id='cust_bottom_p2', component_property='figure'),
    [Input(component_id='dt_range_p2', component_property='start_date'),
     Input(component_id='dt_range_p2', component_property='end_date'),
     Input(component_id='country_dropdown_p2', component_property='value'),
     Input(component_id='stock_cd_dropdown_p2', component_property='value')],

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

        cust_dist = dfv_fltrd.groupby(['Description']).agg({'CustomerID':lambda x:x.nunique()}).reset_index()
        cust_dist = cust_dist.sort_values(['CustomerID'], ascending=True)
        cust_dist = cust_dist[:10]
        fig4 = px.bar(cust_dist, x='Description', y="CustomerID")
        fig4.update_layout(
            title="Bottom 10 Stocks by Customer Count",
            xaxis_title="Stocks Description",
            yaxis_title="# Customers")
        return fig4





