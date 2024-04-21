#Reference: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash%20Components/Graph/dash-graph.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()
print(df.head())

c = dict(zip(df["country"].unique(), px.colors.qualitative.G10))
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True, options=[{'label': x, 'value': x} for x in df.country.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None, selectedData=None,
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': True,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  ),
        dcc.Graph(id = "bar-graph",figure={}, className='six columns',style={'margin':'10px'})
    ])
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    #print(dff)
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country',  hover_data=["lifeExp", "pop", "iso_alpha"]
                  , color_discrete_map= c)
    fig.update_traces(mode='lines+markers')
    return fig

# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, country_chosen):
    if hov_data is None:
        dff2 = df[df.country.isin(country_chosen)]
        dff2 = dff2[dff2.year == 1952]
        #print(dff2)
        fig2 = px.pie(data_frame=dff2, 
                      values='pop', 
                      names='country',
                      color='country',
                      title='Population for 1952', 
                      color_discrete_map=c)
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(data_frame=dff2,
                      values='pop',
                      names='country',
                      title=f'Population for: {hov_year}',
                      color='country', 
                      color_discrete_map=c)
        return fig2

@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)

def update_bar_chart(slct_data,country_chosen):
    if slct_data:
        slct_year = [point['x'] for point in slct_data['points']]
        dff3 = df[df.country.isin(country_chosen) & df.year.isin(slct_year)]
        fig3 = px.bar(
            data_frame=dff3, 
            x='year', 
            y='gdpPercap',
            barmode='group',
            title='GDP Per Capita', 
            color='country', 
            color_discrete_map=c
        )
        return fig3
    else:
        dff3 = df[df.country.isin(country_chosen)]
        fig3 = px.bar(data_frame=dff3, 
                      x='year', 
                      y='gdpPercap',
                      color='country',  
                      barmode='group', 
                      title='GDP Per Capita',
                      color_discrete_map=c
        )
        return fig3



if __name__ == '__main__':
    app.run_server(debug=True, port = 1111)