import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

# import dash_core_components as dcc
# import dash_html_components as html

import numpy as np

from jmspack.utils import apply_scaling
from utils import request_mobility_data_url, summary_window_FUN


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.layout = html.Div([
    html.H1(id='H1', children='Energy Price Calculation', 
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
    html.I("Input the energy price in euro/kwh"),
    html.Div([
        dcc.Input(
                id="energy_amount",
                type="number",
                value=0.262),
    ], style={'width': '100%', 'display': 'inline-block', "color": "#222", "padding": "10px"}),
    html.I("Input the gas price in euro/kwh"),
    html.Div([
        dcc.Input(
                id="gas_price",
                type="number",
                value=1),
    ], style={'width': '100%', 'display': 'inline-block', "color": "#222", "padding": "10px"}),
    html.I("Input the electricity price in euro/kwh"),
    html.Div([
        dcc.Input(
                id="electricity_price",
                type="number",
                value=0.3),
    ], style={'width': '100%', 'display': 'inline-block', "color": "#222", "padding": "10px"}),
    html.I("Input the amount of hours you use the energy for per day"),
    html.Div([
        dcc.Input(
                id="hours_used",
                type="number",
                value=1),
    ], style={'width': '100%', 'display': 'inline-block', "color": "#222", "padding": "10px"}),

    html.I("Input the amount of space used"),
    html.Div([  
        dcc.Input(
                id="space_for_energy",
                type="number",
                value=1),
    ], style={'width': '100%', 'display': 'inline-block', "color": "#222", "padding": "10px"}),

    html.Div(dcc.Graph(id='bar_prices'), 
    style={"margin-left": "auto", "margin-right": "auto", 'width': '80%', 'display': 'block'}),

    html.Div(dcc.Graph(id='graph_range_update'), 
    style={"margin-left": "auto", "margin-right": "auto", 'width': '80%', 'display': 'block'}),
    # html.P(id='P_note', children='''INFO: to hide lines click the marker in the legend''',
    #             style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 10}),

    html.Div(id="output", style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40})
],
)

@app.callback(
    Output("output", "children"),
    Input("energy_amount", "value"),
    Input("hours_used", "value"),
    Input("space_for_energy", "value"),
    
)
def update_output(energy_amount, hours_used, space_for_energy):
    return u'energy_amount = {}, hours_used = {}, space_for_energy = {}' .format(energy_amount, hours_used, space_for_energy)


@app.callback(
    Output("bar_prices", "figure"),
    Input("gas_price", "value"),
    Input("electricity_price", "value"),
)
def bar_prices(gas_price, electricity_price):
    df = pd.DataFrame({"provider": ["user_choice", "essent", "vattenfall", "eneco"],
    "gas_price": [gas_price, 1.11, 1.259, 1.80],
    "electricity_price": [electricity_price, 0.25, 0.236, 0.49]})

    fig = px.bar(df.melt(id_vars="provider"), x="provider", y="value", color="variable")

    fig.update_layout(title='Energy Prices',
                      xaxis_title="Provider",
                      yaxis_title='Price per cubic meter/ or kilowatt hour',
                      paper_bgcolor='rgb(34, 34, 34)',
                          plot_bgcolor='rgb(34, 34, 34)',
                          template="plotly_dark",
                      )

    return fig

@app.callback(
    Output("graph_range_update", "figure"),
    Input("energy_amount", "value"),
    Input("hours_used", "value"),
    Input("space_for_energy", "value"),
    
)
def graph_range_update(energy_amount, hours_used, space_for_energy):

    plot_df = pd.DataFrame({
    "hours_used": np.arange(hours_used, hours_used+5, step=0.5),
    }).assign(**{
        "provider": lambda x: np.repeat("user_choice", repeats=x.shape[0]),
        "energy_range": lambda x: np.repeat(energy_amount, repeats=x.shape[0]),
        "price_per_day": lambda x: x["energy_range"] * x["hours_used"] *  space_for_energy})
   
    # fig=go.Figure([
    # go.Scatter(
    #     name='Energy Calculation',
    #     x=plot_df['energy_range'],
    #     y=plot_df['hours_used'],
    #     mode='lines',
    #     line=dict(color='rgb(31, 119, 180)'),
    # ),
    # ])

    fig = px.line(plot_df, x='price_per_day', y='hours_used', markers=True)

    fig.update_layout(title='Energy Prices Per Hours Used',
                      xaxis_title='Price Per Day',
                      yaxis_title='Hours Used',
                      paper_bgcolor='rgb(34, 34, 34)',
                          plot_bgcolor='rgb(34, 34, 34)',
                          template="plotly_dark",
                      )

    return fig

# @app.callback(Output(component_id='multi_line_plot', component_property='figure'),
#               [Input(component_id='region_choice', component_property='value'),
#               ]
#               )
# def graph_update_multi(region_choice):

    # plot_df = (prep_df
    #                .filter(regex=region_choice)
    #                .reset_index()
    #                .melt(id_vars="index")
    # )
    # fig = px.line(
    #     data_frame=plot_df,
    #     x='index',
    #     y="value",
    #     color="variable",
    #     markers=True
    # )
    # # fig.update_traces(line_color='#743de0')

    # fig.update_layout(title='Mobility == {}'.format(region_choice),
    #                   xaxis_title='Date',
    #                   yaxis_title='{}'.format(region_choice),
    #                   paper_bgcolor='rgb(34, 34, 34)',
    #                       plot_bgcolor='rgb(34, 34, 34)',
    #                       template="plotly_dark",
    #                   )
    # return fig


if __name__ == '__main__':
    app.run_server(debug=False)
