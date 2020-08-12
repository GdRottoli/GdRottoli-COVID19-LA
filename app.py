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
    'deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
    'recovered': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'}

df_confirmed = pd.read_csv(data_url['confirmed'])
df_confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_confirmed = df_confirmed.groupby('Country/Region').sum()
countries = df_confirmed.index.values
df_confirmed = df_confirmed.T

df_deaths = pd.read_csv(data_url['deaths'])
df_deaths.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_deaths = df_deaths.groupby('Country/Region').sum()
df_deaths = df_deaths.T

df_recovered = pd.read_csv(data_url['recovered'])
df_recovered.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_recovered = df_recovered.groupby('Country/Region').sum()
df_recovered = df_recovered.T

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
                        id='yaxis-type-11',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-11')),

                    html.H2('Desde el primer caso en cada país'),
                    dcc.RadioItems(
                        id='yaxis-type-12',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-12')),

                    html.H2('Casos semanales Vs Cantidad total'),
                    dcc.RadioItems(
                        id='yaxis-type-13',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-13')),
                ]),
                dcc.Tab(label='Velocidad de Contagio', children=[
                    html.H2('Tiempo de duplicación de contagio'),
                    dcc.RadioItems(
                        id='yaxis-type-21',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-21')),

                    html.H2('Casos por día'),
                    dcc.RadioItems(
                        id='yaxis-type-22',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-22'))
                ]),

                dcc.Tab(label='Casos Activos', children=[
                    html.H2('Casos activos totales'),
                    dcc.RadioItems(
                        id='yaxis-type-31',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-31')),

                    html.H2('Recuperados totales'),
                    dcc.RadioItems(
                        id='yaxis-type-32',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-32')),

                    html.H2('Casos recuperados diarios'),
                    dcc.RadioItems(
                        id='yaxis-type-33',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-33'))
                ]),
                dcc.Tab(label='Fallecidos', children=[

                    html.H2('Personas fallecidas'),
                    dcc.RadioItems(
                        id='yaxis-type-41',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-41')),

                    html.H2('Personas fallecidas por día'),
                    dcc.RadioItems(
                        id='yaxis-type-42',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-42')),

                    html.H2('Letalidad'),
                    dcc.RadioItems(
                        id='yaxis-type-43',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(id=('graph-43')),

                ])

            ])
        ]
    ),
    html.Div(
        children='Por Giovanni D. Rottoli (gd.rottoli@gmail.com), datos de https://github.com/CSSEGISandData/COVID-19')
])

@app.callback(
    Output('graph-11', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-11', 'value')])
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
    Output('graph-12', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-12', 'value')]
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
    Output('graph-13', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-13', 'value')]
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
    Output('graph-21', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-21', 'value')]
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
    Output('graph-22', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-22', 'value')]
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

@app.callback(
    Output('graph-31', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-31', 'value')]
)
def update_figure_actives_byday(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        confirmed = df_confirmed[c]
        recovered = df_recovered[c]
        deaths = df_deaths[c]
        actives = [x1 - x2 - x3 for (x1, x2, x3) in zip(confirmed, recovered, deaths)]
        first_day = next(i for i, v in enumerate(actives) if v > 0)
        values = actives[first_day:]
        fig.add_trace(go.Scatter(x=np.arange(len(values)), y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Casos activos",
    )
    return fig

@app.callback(
    Output('graph-32', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-32', 'value')]
)
def update_figure_recuperados_totales(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        confirmed = df_confirmed[c]
        first_day = next(i for i, v in enumerate(confirmed) if v > 0)

        recovered = df_recovered[c]
        values = recovered[first_day:]
        fig.add_trace(go.Scatter(x=np.arange(len(values)), y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Personas recuperadas",
    )
    return fig

@app.callback(
    Output('graph-33', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-33', 'value')]
)
def update_figure_recuperados_pordia(selected_countries, yaxis_type):
    data = []
    for c in selected_countries:
        confirmed = df_confirmed[c]
        first_day = next(i for i, v in enumerate(confirmed) if v > 0)
        recovered = df_recovered[c].tolist()
        values = [t - s for s, t in zip(recovered, recovered[1:])]
        data.append(go.Bar(name=c, x=np.arange(len(values)), y=values))
    fig = go.Figure(data=data)
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Personas recuperadas por día",
    )
    return fig

@app.callback(
    Output('graph-41', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-41', 'value')]
)
def update_figure_fallecidos_totales(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        confirmed = df_confirmed[c]
        first_day = next(i for i, v in enumerate(confirmed) if v > 0)

        deaths = df_deaths[c]
        values = deaths[first_day:]
        fig.add_trace(go.Scatter(x=np.arange(len(values)), y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Personas fallecidas",
    )
    return fig

@app.callback(
    Output('graph-42', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-42', 'value')]
)
def update_figure_fallecidas_pordia(selected_countries, yaxis_type):
    data = []
    for c in selected_countries:
        confirmed = df_confirmed[c]
        first_day = next(i for i, v in enumerate(confirmed) if v > 0)
        deaths = df_deaths[c].tolist()
        values = [t - s for s, t in zip(deaths, deaths[1:])]
        data.append(go.Bar(name=c, x=np.arange(len(values)), y=values))
    fig = go.Figure(data=data)
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Personas recuperadas por día",
    )
    return fig

@app.callback(
    Output('graph-43', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type-43', 'value')]
)
def update_figure_letalidad(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        confirmed = df_confirmed[c]
        first_day = next(i for i, v in enumerate(confirmed) if v > 0)
        deaths = df_deaths[c].tolist()
        values = [t*100/s for s, t in zip(confirmed[first_day:], deaths[first_day:])]
        fig.add_trace(go.Scatter(x=np.arange(len(values)), y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    fig.update_layout(
        xaxis_title="Días desde el primer caso",
        yaxis_title="Porcentaje de Letalidad",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
