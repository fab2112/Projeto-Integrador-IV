# Imports
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from utils.theme_switch import ThemeSwitch
from settings import *
from dash import html
import dash_bootstrap_components as dbc


# Datepicker
dmc_datepicker_1 = dmc.DatePicker(
    id="date-picker-1",
    #label="Data inicial",
    description="Data Inicial",
    clearable=False,
    value=primeiro_dia_mes_anterior,
    style={"width": '50%'},
    inputFormat="MMM - DD, YYYY",
    locale='pt-br',)

dmc_datepicker_2 = dmc.DatePicker(
    id="date-picker-2",
    #label="Data final",
    description="Data Final",
    clearable=False,
    value=dia_corrente,
    style={"width": '50%'},
    inputFormat="MMM - DD, YYYY",
    locale='pt-br',)

datepicker_group = dmc.MantineProvider(
    dmc.Group(
        id='datepicker-group-1',
        spacing="lg",
        position='apart',
        noWrap=True,
        children=[dmc_datepicker_1, dmc_datepicker_2],), 
    theme={"colorScheme": "light"},
    id="dp-theme",)


# Update Button - Dash Mantine Components
update_button = dmc.Button("Atualizar",
                           id="loading-button",
                           #compact=True,
                           variant="outline",
                           radius=5,
                           loading=False,
                           color="red",
                           #fullWidth=True,
                           leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled", height=18, width=18),
                           style={"margin":"0px",
                                  "margin-top": "0px",
                                  "margin-right":"0px",
                                  "padding": "10px",
                                  }
                           ),


# Swicth theme
theme_switch = html.Div([ThemeSwitch(aio_id="theme-2", themes=[dbc_theme_light, dbc_theme_dark])],
                        style={"margin":"0px",
                               "padding": "0px",
                               "text-align": "right",
                               "white-space": "nowrap",
                               "display": "flex",
                               "justify-content": "right"})


# Navbar header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(
                                id="logo-1",
                                src='assets/logo_univesp.png'),
                        ), md="auto", style={"text-align": "left"}
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3("Dashboard de Análise Financeira ", id='title-1'),
                                    html.Hr(id='hrline'),
                                    html.P("Projeto Gestão Inteligente - Projeto Integrador IV 2023", id='subtitle-1'),                                                               
                                ],
                            )
                        ],
                        md='auto',
                        align="right",
                    ),
                    
                ],
                align="center"),

            dbc.Row(
                [
                    dbc.Col(update_button, md=2, sm=12, style={"margin":"0px","padding": "0px", "text-align": "right"}),
                    dbc.Col(md=1, sm=12, style={"margin-left":"0px"}),
                    dbc.Col([html.Div(datepicker_group)], md=7, sm=12, style={"margin":"0px","padding": "0px"}),
                    dbc.Col([html.Div(theme_switch, style={"text-align": "right"})], md=2, sm=12,
                            style={"margin":"0px", "padding": "0px"})

                ], align="center")

        ],
        fluid=True,
    ),
    color="#2c3e50",
    dark=False,
    #sticky='top',
    class_name='navbar navbar-expand-lg navbar-light')