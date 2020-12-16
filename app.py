import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os
from data_creator import check_ticker, data_model

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, './data/output/tech_data.csv')
tech_data = pd.read_csv(my_file)


# Initialise the app
app = dash.Dash(__name__)


# Create a list of dictionaries
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks['ticker']:
        dict_list.append({'label': i, 'value': i})

    return dict_list


@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
        # STEP 1
    df_sub, p = data_model(str(selected_dropdown_value).strip("'[]'"))
    # STEP 2
    # Draw and append traces for each stock
    data = [go.Scatter(x=df_sub['Date'],
                                y=df_sub['Price'],
                                name=selected_dropdown_value,
                                showlegend=True,
                                fill='tozeroy',
                                mode='lines',
                                opacity=0.7,
                                textposition='bottom center')]

    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=['#27C1FF', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': f'{selected_dropdown_value}', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub['Date'].min(), df_sub['Date'].max()]},
              ),
              }

    return figure

@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''

    df_sub, p = data_model(str(selected_dropdown_value).strip("'[]'"))
    trace = []
    # Draw and append traces for each stock
    trace.append(go.Scatter(x=df_sub['Date'],
                                 y=df_sub['RSI'],
                                 name='RSI',
                                 showlegend=True,
                                 mode='lines',
                                 opacity=0.7,
                                 textposition='bottom center'))

    fig = px.scatter(x=df_sub['Date'],
                     y=df_sub['RSI'],)

    fig.add_hline(y=30, line_width=3, line_color='green', line_dash='dash')

    trace.append(fig)

    traces = [trace]
    data = [val for sublist in traces for val in sublist]


    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                          colorway=['#FFAA27', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                          template='plotly_dark',
                          paper_bgcolor='rgba(0, 0, 0, 0)',
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          margin={'t': 50},
                          height=400,
                          hovermode='x',
                          autosize=True,
                          title={'text': 'RSI', 'font': {'color': 'white'}, 'x': 0.5},
                          xaxis={'showticklabels': True, 'range': [df_sub['Date'].min(), df_sub['Date'].max()]}),
              }


    return figure


# Define the app:
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls', children = [
                                            html.H2('STOCK PRICES SELECTION'),
                                            html.P('''Choose any stock to see its historic price'''),
                                            html.P('''You will be able to visualize the stock price and its RSI'''),
                                            html.Div(className='div-for-dropdown',
                                                     children=[
                                                     dcc.Dropdown(id='stockselector',
                                                                  options=get_options(tech_data),
                                                                  multi=False,
                                                                  value=tech_data['ticker'].sort_values()[0],
                                                                  style={'backgroundColor': '#1E1E1E'},
                                                                  className='stockselector')
                                                                ],
                                                     style={'color': '#1E1E1E'})
                                        ]),
                                  html.Div(className='eight columns div-for-charts bg-grey', children = [
                                            dcc.Graph(id='timeseries', config={'displayModeBar': False}),
                                            dcc.Graph(id='change', config={'displayModeBar': False})]
                                    )]),
                                  ])






# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
