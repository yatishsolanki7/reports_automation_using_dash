
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import warnings
warnings.filterwarnings("ignore")

from app import app
from apps import page1, page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('MIS & Country wise distribution | ', href='/apps/page1'),
        dcc.Link('Top/Bottom 10 Stocks by Sales', href='/apps/page2'),
    ], className="row"),
    html.Div(id='page-content', children=[])

])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/page1':
        return page1.layout
    elif pathname == '/apps/page2':
        return page2.layout
    else:
        return 'Please choose a link from above'

if __name__ == '__main__':
    # app.run_server(debug=True,port=4065)
    app.run_server(debug=False)

