import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

data_url = {
    'confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
    'deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'}

df_confirmed = pd.read_csv(data_url['confirmed'])
df_confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_confirmed = df_confirmed.groupby('Country/Region').sum()
countries = df_confirmed.index.values
df_confirmed = df_confirmed.T

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFFFF',
    'text': '#81BEF7'
}

app.layout = html.Div(className="container", children = [
    html.Div(
        html.H1(children='COVID-19',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                })
    ),
    html.Div(
        children=[
            html.Div(children=[
                html.Label('Seleccionar paises'),
                html.Div(
                dcc.Dropdown(
                        id='drop-country-list',
                        options=[{'label': i, 'value': i} for i in countries],
                        value=['Argentina', 'Brazil'],
                        multi=True
                    )
                )
            ]),
            dcc.Tabs([
                dcc.Tab(label='Tendencia de Contagios', children=[
                    html.H2('Desde 01-22-2020'),
                    dcc.RadioItems(
                        id='yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-time-serie')),
                    html.H2('Desde el primer caso en cada país'),
                    dcc.RadioItems(
                        id='yaxis-type-day',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-time-serie-day')),
                    html.H2('Casos semanales Vs Cantidad total'),
                    dcc.RadioItems(
                        id='yaxis-type-semanal-diario',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-semanal-diario')),
                ]),
                dcc.Tab(label='Velocidad de Contagio', children=[
                    html.H2('Tiempo de duplicación de contagio'),
                    dcc.RadioItems(
                        id='yaxis-type-vel-contagio',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-vel-contagio')),
                    html.H2('Casos por día'),
                    dcc.RadioItems(
                        id='yaxis-type-contagio-pordia',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-contagio-pordia'))
                ])
            ])
        ]
    ),
    html.Div(
        children='Por Giovanni D. Rottoli (gd.rottoli@gmail.com), datos de https://github.com/CSSEGISandData/COVID-19')
])

@app.callback(
    Output('graph-time-serie', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type', 'value')])
def update_figure(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        fig.add_trace(go.Scatter(x=df_confirmed.index.values, y=df_confirmed[c], mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad de casos",
    )
    return fig


@app.callback(
    Output('graph-time-serie-day', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-day', 'value')]
)
def update_figure_byday(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        values = [elemento for elemento in df_confirmed[c] if elemento > 0]
        fig.add_trace(go.Scatter(x=np.arange(len(values)), y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Cantidad de días desde el primer caso",
        yaxis_title="Cantidad de casos totales registrados",
    )
    return fig

@app.callback(
    Output('graph-vel-contagio', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-vel-contagio', 'value')]
)
def update_figure_vel_contagio(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        values = [elemento for elemento in df_confirmed[c] if elemento > 0]
        minval = values[0]
        i = 0
        countvalues = []
        for val in values:
            if val >= 2*minval:
                minval = val
                countvalues.append(i)
                i = 1
            else:
                i = i+1
        fig.add_trace(go.Scatter(x=np.arange(len(countvalues)), y=countvalues, mode='lines+markers', name=c))
    fig.update_layout(
        xaxis_title="Cantidad de veces que se duplicaron los casos",
        yaxis_title="Días",
    )
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    return fig

@app.callback(
    Output('graph-semanal-diario', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-semanal-diario', 'value')]
)
def update_figure_semanal_diario(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        cases = [elemento for elemento in df_confirmed[c] if elemento > 0]
        week = [0,0,0,0,0,0,0]
        i = 0
        previous_value = 0
        week_cases = []
        for case in cases:
            difference = abs(case - previous_value )
            week[i%7] = difference
            week_cases.append(sum(week))
            previous_value = case
            i = i + 1
        fig.add_trace(go.Scatter(x=cases, y=week_cases, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Casos totales",
        yaxis_title="Casos semanales",
    )
    return fig

@app.callback(
    Output('graph-contagio-pordia', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-contagio-pordia', 'value')]
)
def update_figure_tendencia_contagio_pordia(selected_countries, yaxis_type):
    data = []
    for c in selected_countries:
        cases = [elemento for elemento in df_confirmed[c] if elemento > 0]
        previous_value = 0
        daily_cases = []
        for case in cases:
            daily_cases.append(case - previous_value)
            previous_value = case
        data.append(go.Bar(name=c, x=np.arange(len(daily_cases)), y=daily_cases ))
    fig = go.Figure(data= data)
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Día",
        yaxis_title="Casos diarios",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
