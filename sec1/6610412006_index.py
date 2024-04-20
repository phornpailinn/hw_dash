import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from app import app
from apps import scatter_layout, histogram_layout, line_layout, treemap_layout

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Scatter | ", href="/apps/scatter_layout", active="exact"),
                dbc.NavLink("Histogram | ", href="/apps/histogram_layout", active="exact"),
                dbc.NavLink("Treemap | ", href="/apps/treemap_layout", active="exact"),
                dbc.NavLink("LineChart | ", href="/apps/line_layout", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


    

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/apps/scatter_layout':
        return html.P(scatter_layout.layout)
    if pathname == '/apps/histogram_layout':
        return html.P(histogram_layout.layout)
    if pathname == '/apps/treemap_layout':
        return html.P(treemap_layout.layout)
    if pathname == '/apps/line_layout':
        return html.P(line_layout.layout)
    if pathname == '/':
        return html.P("Please choose a link")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
     app.run_server(port=8888)
    
#Exercise
# 1. Change menu3 to another graph (Not histogram)
# 2. Add the 4th menu (menu4) link to line graph
