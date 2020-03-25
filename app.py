import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_url= {'confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
           'deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'}

countries = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Cuba', 'Ecuador', 'Germany', 'Guatemala','Italy','Japan','Korea, South','Mexico', 'Panama',
             'Paraguay', 'Peru', 'Spain', 'Uruguay' ]

df_confirmed = pd.read_csv(data_url['confirmed'])
df_confirmed = df_confirmed[df_confirmed['Country/Region'].isin(countries)]
df_confirmed = df_confirmed.drop(columns=['Province/State','Lat','Long'])
df_confirmed = df_confirmed.set_index(['Country/Region'])
df_confirmed = df_confirmed.T

#df_confirmed = df_confirmed.iloc[50:]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFF',
    'text': '#81BEF7'
}

app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='COVID-19 in Latinoamerica',
                style={
                 'textAlign': 'center',
                 'color': colors['text']
        }),
        html.Label('Select countries (Some asian and eurupean countries are included for reference purposes)'),
        dcc.Dropdown(
            id='drop-country-list',
            options=[{'label': i, 'value': i} for i in countries],
            value=['Argentina', 'Brazil'],
            multi=True
        ),
        html.H2('Since 01-22-2020'),
        dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id=('graph-time-serie')),
        html.H2('Since the first case in each country'),
        dcc.RadioItems(
            id='yaxis-type-day',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id=('graph-time-serie-day')),
        html.Footer(
            children='By Giovanni D. Rottoli (gd.rottoli@gmail.com), data from https://github.com/CSSEGISandData/COVID-19'
        )
    ]
)

@app.callback(
    Output('graph-time-serie', 'figure'),
    [Input('drop-country-list', 'value'),
     Input('yaxis-type', 'value')]
)
def update_figure(selected_countries, yaxis_type):
    fig = go.Figure()
    for c in selected_countries:
        fig.add_trace(go.Scatter(x=df_confirmed.index.values, y=df_confirmed[c], mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
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
        fig.add_trace(go.Scatter(x= np.arange(len(values)) , y=values, mode='lines+markers', name=c))
    if (yaxis_type == 'Log'):
        fig.update_layout(yaxis_type="log")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)