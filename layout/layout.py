# Imports
from dash import html
from dash import dcc
from settings import config_g
from settings import gutter_row
from .layout_components import header
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


# Dash Layout
layout_ = dbc.Container([
      
    dcc.Store(id='data-store-1'),
    
    header,

    dbc.Tabs([

        dbc.Tab([

            # Linha 1
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-1", className='card-title'), html.Hr(className='line-card'),
                        dcc.Dropdown(id="dropdown-8",
                                     options=['Contas combinadas', 'Bradesco', 'Nubank', 'Banco Brasil',
                                              'BTG', 'Caixa', 'Banco Inter'],
                                     value='Contas combinadas',
                                     clearable=False,
                                     placeholder="Selecione uma conta"), html.Div([
                                         dcc.RadioItems(['Dia', 'Semana', 'Mês', 'Trimestre'], 'Dia', inline=True, id="radioitem-1",
                                                        labelStyle={'margin-right': '20px',
                                                                    "margin-bottom": "-10px"},
                                                        inputStyle={"margin-right": "6px",
                                                                    "margin-bottom": "-10px"}),
                                         html.Div(style={'width': '20px'}),
                                         dcc.RadioItems(['Crédito', 'Débito', 'Todos'], 'Todos', inline=True, id="radioitem-13",
                                                        labelStyle={'margin-right': '20px',
                                                                    "margin-bottom": "-10px",},
                                                        inputStyle={"margin-right": "6px",
                                                                    "margin-bottom": "-10px"})], style={'display': 'flex',
                                                                                                        'margin-top': '5px',
                                                                                                        'flex-direction': 'row',
                                                                                                        'justify-content': 'center'}),
                        dcc.Loading(dcc.Graph(id='chart-1-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=8, sm=12, style={"display": "grid"}),


                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-6", className='card-title'), html.Hr(className='line-card'),
                        html.Div([
                            dcc.Dropdown(id="dropdown-5",
                                 clearable=False,
                                 placeholder="Selecione um Credor"),
                            dcc.RadioItems(['Débito', 'Crédito'], 'Débito', inline=True, id="radioitem-6",
                                           labelStyle={'margin-right': '20px',
                                                       "margin-bottom": "-10px"},
                                           inputStyle={"margin-right": "6px",
                                                       "margin-bottom": "-10px"}),
                        ]),
                        dcc.Loading(dcc.Graph(id='chart-6-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ],
                        outline=True, class_name='dbc')], lg=4, sm=12, style={"display": "grid"}),


            ], class_name=gutter_row),


            # Linha 2
            dbc.Row([
                
                
                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-4", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(html.H4(id='chart-4-px', style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=9, sm=12, style={"display": "grid"}),

                
                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-2", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Débito', 'Crédito'], 'Débito', inline=True, id="radioitem-3",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-2-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=12, style={"display": "grid"}),


            ], class_name=gutter_row),


            # Linha 3
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-8", className='card-title'), html.Hr(className='line-card'),
                        html.Div([
                            dcc.Dropdown(id="dropdown-6",
                                 clearable=False,
                                 placeholder="Selecione um Credor"),
                            dcc.RadioItems(['Débito', 'Crédito'], 'Débito', inline=True, id="radioitem-5",
                                           labelStyle={'margin-right': '20px',
                                                       "margin-bottom": "-10px"},
                                           inputStyle={"margin-right": "6px",
                                                       "margin-bottom": "-10px"}),
                        ]),
                        dcc.Loading(dcc.Graph(id='chart-8-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ],
                        outline=True, class_name='dbc')], lg=6, sm=12, style={"display": "grid"}),


                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-5", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-5-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=6, style={"display": "grid"}),


                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-3", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Débito', 'Crédito'], 'Débito', inline=True, id="radioitem-4",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-3-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=6, style={"display": "grid"}),


            ], class_name=gutter_row),


        ], label="Movimentações Financeira",
            id="tab-1",
            active_label_class_name="text-primary",
            label_style={'color': 'grey'},),
        

        dbc.Tab([


            # Linha 1
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-9", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Mês', 'Trimestre'], 'Mês', inline=True, id="radioitem-7",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-9-px', config=config_g,
                                              style={'visibility': 'hidden',},), type='default'),

                    ], outline=True, class_name='dbc')], lg=4, sm=6, style={"display": "grid"}),
                
                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-14", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-14-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc', body=True)], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-15", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-15-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=5, sm=12, style={"display": "grid"}),


            ], class_name=gutter_row),

            # Linha 2
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-11", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Mês', 'Trimestre'], 'Mês', inline=True, id="radioitem-9",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-11-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], md=4, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-12", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Mês', 'Trimestre'], 'Mês', inline=True, id="radioitem-10",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-12-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], md=4, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-10", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Mês', 'Trimestre'], 'Mês', inline=True, id="radioitem-8",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-10-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], md=4, style={"display": "grid"}),


            ], class_name=gutter_row),

            # Linha 3
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-16", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Despesas', 'Faturamento'], 'Despesas', inline=True, id="radioitem-12",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-16-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-17", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-17-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=4, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-13", className='card-title'), html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-13-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=5, sm=12, style={"display": "grid"}),
                    
            ], class_name=gutter_row),


        ], label="Faturamento, Despesas e Lucro",
                id="tab-2",
            active_label_class_name="text-primary",
            label_style={'color': 'grey'}),

        dbc.Tab([

            # Text cards - Linha 1
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo contas combinadas',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-1-2"),
                    ], outline=True, id='card-text-1', )], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo Banco Brasil', className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-2-2"),
                    ], outline=True, id='card-text-2')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo Bradesco',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-3-2"),
                    ], outline=True, id='card-text-3')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo Nubank', className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-4-2"),
                    ], outline=True, id='card-text-4')], lg=3, sm=6, style={"display": "grid"}),

            ], class_name=gutter_row),
            
            # Text cards - Linha 2
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo BTG',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-5-2"),
                    ], outline=True, id='card-text-5')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo Caixa',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-6-2"),
                    ], outline=True, id='card-text-6')], lg=3, sm=6, style={"display": "grid"}),
                
                dbc.Col([
                    dbc.Card([
                        html.Div('Saldo Banco Inter', className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-7-2"),
                    ], outline=True, id='card-text-7')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Recebimentos atrasados',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-8-2"),
                    ], outline=True, id='card-text-8')], lg=3, sm=6, style={"display": "grid"}),

            ], class_name=gutter_row),
            
            # Text cards - Linha 3
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div('Pagamentos atrasados',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-9-2"),
                    ], outline=True, id='card-text-9')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Recebimentos previstos',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-10-2"),
                    ], outline=True, id='card-text-10')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Pagamentos previstos',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-11-2"),
                    ], outline=True, id='card-text-11')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div('Faturamento do período',
                                className='card-title-text'),
                        html.Hr(className='line-card'),
                        html.Div(id="card-text-12-2"),
                    ], outline=True, id='card-text-12')], lg=3, sm=6, style={"display": "grid"}),

            ], class_name=gutter_row),

            # Gráficos - Linha 3
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-18", className='card-title'), html.Hr(className='line-card'),
                        dcc.Slider(id='slider-1', min=1, step=10, marks=None,
                                   tooltip={"placement": "right", "always_visible": False}),
                        dcc.Loading(dcc.Graph(id='chart-18-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-19", className='card-title'), html.Hr(className='line-card'),
                        dcc.Slider(id='slider-2', min=1, step=100, marks=None,
                                   tooltip={"placement": "right", "always_visible": False}),
                        dcc.Loading(dcc.Graph(id='chart-19-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=3, sm=6, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-20", className='card-title'), html.Hr(className='line-card'),
                        dcc.RadioItems(['Faturamento', 'Despesas'], 'Faturamento', inline=True, id="radioitem-14",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-20-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=6, sm=12, style={"display": "grid"}),


            ], class_name=gutter_row),

            # Gráficos - Linha 3
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-21", className='card-title'),
                        html.Hr(className='line-card'),
                        dcc.RadioItems(['Crédito', 'Débito'], 'Crédito', inline=True, id="radioitem-15",
                                       labelStyle={'margin-right': '20px',
                                                   "margin-bottom": "-10px"},
                                       inputStyle={"margin-right": "6px",
                                                   "margin-bottom": "-10px"}),
                        dcc.Loading(dcc.Graph(id='chart-21-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=5, sm=12, style={"display": "grid"}),

                dbc.Col([
                    dbc.Card([
                        html.Div(
                            id="card-title-22", className='card-title'),
                        html.Hr(className='line-card'),
                        dcc.Loading(dcc.Graph(id='chart-22-px', config=config_g,
                                              style={'visibility': 'hidden'}), type='default'),

                    ], outline=True, class_name='dbc')], lg=7, sm=12, style={"display": "grid"}),


            ], class_name=gutter_row),


        ], label="Indicadores de Performance e Análise de Atrasos",
                id="tab-3",
            active_label_class_name="text-primary",
            label_style={'color': 'grey'}),

    ], id='tabs'),
    
    dmc.MantineProvider(
        dmc.NotificationsProvider(html.Div(id="notify-container"), position="top-right",), id="note-1")

], fluid=True, id='container')

layout_ = dmc.MantineProvider(layout_)