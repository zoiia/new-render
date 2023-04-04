import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

import plotly.figure_factory as ff

df = pd.read_csv("nyc_new.csv")

df2 = df.melt(id_vars=['Year', 'Month']).groupby(['Year', 'Month', 'variable']).sum().reset_index()

df2.rename(columns={'variable': 'Status', 'value': 'TEUs'}, inplace=True)
df3 = df2.groupby(['Year', 'Month']).agg({'TEUs': sum}).reset_index()
df4 = df

df4['TOTAL TEUs'] = df4['Loaded Imports'] + df4['Empty Imports'] + df4['Loaded Exports'] + df4['Empty Exports']

df5 = df4.groupby(['Year']).sum()

df6 = df2.drop(columns={'Month'})

ordered_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

df7 = df3
df7['to_sort'] = df3['Month'].apply(lambda x: ordered_months.index(x))
df7 = df7.sort_values('to_sort')

df8 = pd.read_csv('trucks.csv')
# print(df8.dtypes)

df9 = df8.drop(columns={'Week'})
df9 = df8.groupby(['Year', 'Month']).agg({'Truck Visits': sum}).reset_index()
df10 = df9
df10['to_sort'] = df9['Month'].apply(lambda x: ordered_months.index(x))
# print(df10)
# print(df5)

df12 = df5
df12 = df5.drop(columns={'Loaded Imports', 'Empty Imports', 'Loaded Exports', 'Empty Exports'}).reset_index()
df13 = df12.head(5)
print(df13)
# df11 = df8
# df11['MonthFirstDay'] = df11['Week Ending'] - pd.to_timedelta(df11['Week Ending'].dt.day - 1, unit='d')
# print(df11)

#
# card1 = dbc.Card([
#     dbc.CardBody([
#         html.H4("Card title", className="card-title", id="card_num1"),
#         html.P(f"BLA BLA BLA ${new}", className="card-text", id="card_text1")
#     ])
# ],
#     style={'display': 'inline-block',
#            'width': '33.3%',
#            'text-align': 'center',
#            'background-color': 'pink'},
#     outline=True)

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewpoint',
                       'content': 'width=device-width initial-scale=1',
                       }])
server = app.server

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1('PORT OF NYNJ - CARGO VOLUMES',
                        className='text-center text-primary, mb-4',
                        style={'font-family': "GT America, sans-serif;",
                               'font-weight': '600', 'font-size': '2.5rem', 'line-height': '3rem',
                               'margin': '50px 50px 60px',
                               'color': 'white',

                               # 'background': '#000080',
                               }

                        ),
                width=12,
                style={
                    'background': '#000080',
                    'margin': '0 0 30px'
                }
                )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="my-dropdown",
                options=
                [{"label": x, "value": x}
                 for x in sorted(df3["Year"].unique())],
                value=[2018, 2019, 2020, 2021, 2022],
                placeholder="Select a year",
                multi=True,
                clearable=False,
                style={'color': 'black'},
            ),

        ], width={'size': 5}),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([

                    html.H4(f"sdfsd", className="border border-primary border-0", id="card_num1"),

                ])
            ], style={'display': 'inline-block',
                      # 'margin-left':50,
                      'width': '120%',
                      'text-align': 'center',
                      # 'background-color':'red',
                      'border': 'blue',
                      },
                outline=False
            )

        ], width={'size': 7}),

    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(id="line-chart", figure={},
                      style={'padding': 10,
                             'margin-left': 10,
                             'margin-right': 20},
                      config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'resetScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian',
                                    'toggleSpikelines',
                                    'resetViewMapbox',
                                    'sendDataToCloud'
                                ],
                                'scrollZoom': False


                      }
                      )

        ], width={'size': 6}),
        # dbc.Col([
        #     # dcc.Graph(id="pie-chart", figure={},
        #     #           )
        #
        # ], width={'size': 0.2}),

        dbc.Col([
            dcc.Graph(id="pie-chart", figure={},
                      style={'padding': 10,
                             'margin-left': 30,
                             'margin-right': 10},
                      config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'resetScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian',
                                    'toggleSpikelines',
                                    'resetViewMapbox',
                                    'sendDataToCloud'
                                ],
                                'scrollZoom': False

                      }
                      )

        ], width={'size': 6})

    ]),

    dbc.Row([

        dbc.Col([

            dcc.Dropdown(
                id="my-drop",
                options=
                [{"label": x, "value": x}
                 for x in sorted(df3["Year"].unique())],
                value=2022,
                multi=False,
                clearable=True,
                style={'color': 'black'}),

        ], width={'size': 2}),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="new-chart", figure={},
                      config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'resetScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian',
                                    'toggleSpikelines',
                                    'resetViewMapbox',
                                    'sendDataToCloud'
                                ],
                                'scrollZoom': False
                        },
                      )

        ], width={'size': 6}),

        dbc.Col([
            dcc.Graph(id="line2-chart", figure={},
                      config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'zoomIn2d',
                                    'zoomOut2d',
                                    'autoScale2d',
                                    'resetScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian',
                                    'toggleSpikelines',
                                    'resetViewMapbox',
                                    'sendDataToCloud'
                                ],
                                'scrollZoom': False
                              },


                      )

        ], width={'size': 6})

    ])

], fluid=True)


@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
#

def update_graph(chosen_value):
    if len(chosen_value) == 0:
        return {}

    else:

        df_filtered = df7[df7["Year"].isin(chosen_value)]
        # print(df_filtered)
        fig = px.line(
            data_frame=df_filtered,
            x="Month",
            y="TEUs",
            height=500,
            color="Year",
            width=650,
            title='Distribution',
            markers=True
            # hover_data={'': ':,'},
            # labels={
            # },
        )
        fig.update_layout(title_text='YEARLY TEUs DISTRIBUTION', title_x=0.5)
        return fig


@app.callback(
    Output(component_id="pie-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def update_graphic(chosen_value):
    if chosen_value == 0:
        return {}

    else:

        df_filtered = df2[df2["Year"].isin(chosen_value)]
        fig = px.pie(data_frame=df_filtered, values='TEUs', names='Status', title='Distribution',
                     color='Status', width=650,
                     height=500, hole=.3,
                     color_discrete_map={'Loaded Imports': '#1a1aff',
                                         'Empty Exports': '#D3D3D3',
                                         'Loaded Exports': '#999999',
                                         'Empty Imports': '#ff1a1a'}

                     )
        fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textposition='outside', textfont_size=14)

        fig.update_layout(showlegend=False)

        fig.update_layout(title_text='TEUs CONTAINER SHARE', title_x=0.5)
        return fig


@app.callback(
    Output(component_id="new-chart", component_property="figure"),
    [Input(component_id="my-drop", component_property="value")],
)
def update_graphic(chosen_value):
    if chosen_value == 0:
        return {}


    else:
        # df_filtered = df3[df3["Year"].isin(chosen_value)]
        df_filtered = df7[df7['Year'] == chosen_value]
        # print(df_filtered)
        fig = px.bar(df_filtered, x="Month", y="TEUs", color="TEUs", width=700, height=450,
                     # color_discrete_map={'TEUs': '#1a1aff'}

                     # color_continuous_scale=px.colors.sequential.Viridis,
                     # hover_data={'Year': 'Year', 'Month': 'Month'},

                     )
        fig.update_traces(opacity=0.80)
        fig.update_layout(title_text='MONTHLY TEUs DISTRIBUTION', title_x=0.5)
        return fig


@app.callback(
    Output(component_id="line2-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def update_graphic(chosen_value):
    if chosen_value == 0:
        return {}


    else:

        #
        # df_filtered = df12[df12["Year"].isin(chosen_value)]
        # # print(df_filtered)
        fig = px.line(df13, x="Year", y="TOTAL TEUs", text="TOTAL TEUs", width=700, height=450)
        fig.update_traces(line=dict(color='royalblue', width=4, dash='dot'))
        fig.update_traces(textposition="bottom center", textfont=dict(family="sans serif", size=16, color="black"))
        fig.update_traces(texttemplate='%{text:.2s}')
        fig.update_layout(title_text='TEUs TRENDLINE 2018 - 2022', title_x=0.5)

        return fig


@app.callback(
    Output('card_num1', 'children'),
    Input('my-dropdown', 'value')
)
def update_cards(chosen_value):
    df_filtered = df7[df7["Year"].isin(chosen_value)]
    # new_df = who_data[(who_data.Country == country_select)]
    new = df_filtered['TEUs'].sum()
    check = str(f'{new:,}')
    return "TOTAL TURNOVER - " + check


if __name__ == "__main__":
    app.run_server(debug=True)
