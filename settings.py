# Imports
import pandas as pd
import numpy as np
import locale
import os
import dash_bootstrap_components as dbc
from datetime import datetime
from dash_bootstrap_templates import template_from_url


producao = False

if producao:
    dataset_path = "/downloads/extrato_financeiro_processado_pi.csv"
    dataset_main_path = "/downloads/extrato_financeiro.xls"
    update_signal_path = "/downloads/update_signal.txt"
    app_path = '/'
    port = 8085
    
else:
    dataset_path = "./downloads/extrato_financeiro_processado_pi.csv"
    dataset_main_path = "./downloads/extrato_financeiro.xls"
    update_signal_path = "./downloads/update_signal.txt"
    app_path = '/'
    port = 80


# Locale configurations
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


# Parâmetros app
app_title = "Dashboard"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


# Variáveis Globais
primeiro_dia_mes_anterior = np.datetime64(datetime(
    datetime.today().year, datetime.today().month - 1, 1).date().strftime('%Y-%m-%d'))
dia_corrente = np.datetime64(datetime.today(), 'D')
file_timestamp = os.path.getmtime(dataset_path)
df_main = pd.read_csv(dataset_path,
                      index_col=[0],
                      encoding='utf8',
                      parse_dates=['data_movimento',
                                   'data_competencia',
                                   'data_original_vencimento',
                                   'data_prevista'])
radioitem_var = 'Mês'
radioitem_var_oper = 'Todos'
conta_var = 'Contas combinadas'
operacao_var = 'Crédito'
inicial_date_var_1 = primeiro_dia_mes_anterior
final_date_var_1 = dia_corrente
inicial_date_var_2 = primeiro_dia_mes_anterior
final_date_var_2 = dia_corrente
theme_light_var = None
theme_dark_var = None


# Parâmetros - charts
fig_margin = dict(l=10, r=10, t=10, b=10)
gridwidth = 1.0
mode_bar = {'orientation': 'h',
            'bgcolor': 'rgba(0,0,0,0)',
            'color': '#D3D3D3',
            'activecolor': 'grey',
            }
dbc_theme_light = dbc.themes.FLATLY
dbc_theme_dark = dbc.themes.CYBORG
theme_light = template_from_url(dbc_theme_light)
theme_dark = template_from_url(dbc_theme_dark)
plotbg_color_light = 'white'
plotbg_color_dark = '#282828'


# Parâmetros layout
gutter_row = 'g-0'
config_g = {'displaylogo': False,
            'modeBarButtonsToRemove': [
                # "zoom2d",
                # "pan2d",
                # "select2d",
                "lasso2d",
                # "zoomIn2d",
                # "zoomOut2d",
                "autoScale2d",
                # "resetScale2d",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "zoom3d",
                "pan3d",
                "resetCameraDefault3d",
                "resetCameraLastSave3d",
                "hoverClosest3d",
                "orbitRotation",
                "tableRotation",
                "zoomInGeo",
                "zoomOutGeo",
                "resetGeo",
                "hoverClosestGeo",
                # "toImage",
                "sendDataToCloud",
                "hoverClosestGl2d",
                "hoverClosestPie",
                "toggleHover",
                "resetViews",
                "toggleSpikelines",
                "resetViewMapbox",
                'drawline',
                'drawopenpath',
                'drawclosedpath',
                'drawcircle',
                'drawrect',
                'eraseshape',
                'hovercompare',
                'hoverCompareCartesian',
                'toggleSpikelines',
                'v1hovermode',
                'hoverclosest',
                'togglehover'
            ],
            'displayModeBar': 'hover',
            'locale': 'pt-br',
            # 'scrollZoom': True,
            'responsive': True,
            }
