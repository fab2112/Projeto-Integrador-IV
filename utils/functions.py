# Imports
import pandas as pd
import numpy as np
import time
import os
import dash_mantine_components as dmc
from datetime import datetime
from time import sleep
from dash_iconify import DashIconify
from dash import callback, Output, Input
from .data_manager import get_dataframe_2
from settings import dataset_main_path, update_signal_path



# ---------- Slider-1 ---------- #
@callback([Output("slider-1", "max"),
               Output("slider-1", "value")],
              [Input("date-picker-1", "value"),
               Input("date-picker-2", "value")])
def slider_val_1(inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)
    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]
    #df_3 = df_3[df_3['descricao'].str.startswith('Venda')]
    df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
    df_4['months_mean'] = df_4.valor_original.mean()

    if not df_4.empty:
        max_ = int(df_4.months_mean[0]) * 2
        value = int(df_4.months_mean[0])
    else:
        max_ = 100
        value = 0
    return [max_, value]


# ---------- Slider-2 ---------- #
@callback([Output("slider-2", "max"),
               Output("slider-2", "value")],
              [Input("date-picker-1", "value"),
               Input("date-picker-2", "value")])
def slider_val_2(inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)
    df_3 = df_2.loc[(df_2.operacao == 'Débito') & (
        df_2.despesas_faturamento == 'despesas')]
    df_3['valor_original'] = df_3.valor_original * -1
    df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
    df_4['months_mean'] = df_4.valor_original.mean()

    if not df_4.empty:
        max_ = int(df_4.months_mean[0]) * 2
        value = int(df_4.months_mean[0])
    else:
        max_ = 100
        value = 0
    return [max_, value]


# ---------- Dropdown-5 chart-6 ---------- #
@callback([Output("dropdown-5", "options"),
               Output("dropdown-5", "value")],
              [Input('radioitem-6', 'value'),
               Input('data-store-1', 'data')])
def dropdown_val_1(contas, data):
    
    df_1 = pd.read_json(data, orient='table')

    options = ['Sem registro']
    value = 'Sem registro'

    try:

        if contas == 'Débito' and len(df_1) != 0:
            df_2 = df_1[df_1.operacao == 'Débito']
            df_3 = df_2.groupby(['fornecedor_cliente'], as_index=False)[
                'valor_original'].sum()
            df_3.sort_values(['valor_original'], ascending=True, inplace=True)
            options = df_3.fornecedor_cliente.unique()
            value = df_3.fornecedor_cliente.unique()[0]

        elif contas == 'Crédito' and len(df_1) != 0:
            df_2 = df_1[df_1.operacao == 'Crédito']
            df_3 = df_2.groupby(['fornecedor_cliente'], as_index=False)[
                'valor_original'].sum()
            df_3.sort_values(['valor_original'], ascending=False, inplace=True)
            options = df_3.fornecedor_cliente.unique()
            value = df_3.fornecedor_cliente.unique()[0]

    except:
        options = ['Sem registro']
        value = 'Sem registro'
    return options, value


# ---------- Dropdown-6 chart-8 ---------- #
@callback([Output("dropdown-6", "options"),
               Output("dropdown-6", "value")],
              [Input('radioitem-5', 'value'),
               Input('data-store-1', 'data')])
def dropdown_val_2(contas, data):
    
    df_ = pd.read_json(data, orient='table')
    df_1 = df_[["operacao", "categoria_nova", "valor_original"]]

    options = ['Sem registro']
    value = 'Sem registro'

    try:

        if contas == 'Débito' and len(df_1) != 0:
            df_2 = df_1[df_1.operacao == 'Débito']
            df_3 = df_2.groupby(['categoria_nova'], as_index=False)[
                'valor_original'].sum()
            df_3.sort_values(['valor_original'], ascending=True, inplace=True)
            options = df_3.categoria_nova.unique()
            value = df_3.categoria_nova.unique()[0]

        elif contas == 'Crédito' and len(df_1) != 0:
            df_2 = df_1[df_1.operacao == 'Crédito']
            df_3 = df_2.groupby(['categoria_nova'], as_index=False)[
                'valor_original'].sum()
            df_3.sort_values(['valor_original'], ascending=False, inplace=True)
            options = df_3.categoria_nova.unique()
            value = df_3.categoria_nova.unique()[0]

    except:
        options = ['Sem registro']
        value = 'Sem registro'
    return options, value
    

# ---------- Update Datepicker by logo click - Refresh Dashboard ---------- #
@callback([Output('date-picker-1', 'value'),
               Output('date-picker-2', 'value'),
               Output('radioitem-1', 'value'),
               Output('dropdown-8', 'value'),
               Output('radioitem-13', 'value'),
               Output('chart-1-px', 'selectedData'),
               Output('chart-21-px', 'selectedData')],
              Input('logo-1', 'n_clicks'))
def update_datepicker_1(n_clicks):
    global primeiro_dia_mes_anterior, dia_corrente
    primeiro_dia_mes_anterior = np.datetime64(datetime(datetime.today().year, datetime.today().month - 1, 1).date().strftime('%Y-%m-%d'))
    dia_corrente = np.datetime64(datetime.today(), 'D')
    periodo_radioitem_1 = 'Dia'
    conta = 'Contas combinadas'
    oper = 'Todos'
    return [primeiro_dia_mes_anterior, dia_corrente, periodo_radioitem_1, conta, oper, None, None]


# ---------- Update ETL - Button ---------- #
@callback(
    [Output("loading-button", "loading"),
     Output("notify-container", "children"),
     Output("date-picker-1", "value", allow_duplicate=True),
     Output("date-picker-2", "value", allow_duplicate=True),],
    Input("loading-button", "n_clicks"),
    prevent_initial_call=True)
def update_etl(n_clicks):
    
    timestamp_start = os.path.getmtime(dataset_main_path)
    
    with open(update_signal_path, "w") as f:
        f.write("True")
        
    while True:
        with open(update_signal_path, "r") as f:
            update_signal = f.read()
            if update_signal == 'False':
                break
        sleep(1.5)
    
    timestamp_end = os.path.getmtime(dataset_main_path)
   
    if timestamp_end > timestamp_start:
        note = dmc.Notification(
            id="my-notification",
            title="Atualização dos dados",
            message="Atualização realizada com sucesso.",
            color="green",
            action="show",
            autoClose=False,
            icon=DashIconify(icon="akar-icons:circle-check"),)
    else:
        note = dmc.Notification(
            id="my-notification",
            title="Atualização dos dados",
            message="Falha durante atualização - tente mais tarde.",
            color="red",
            action="show",
            autoClose=False,
            icon=DashIconify(icon="akar-icons:circle-x"),)
        
    global primeiro_dia_mes_anterior, dia_corrente
    date_1 = np.datetime64(datetime(
        datetime.today().year, datetime.today().month - 1, 1).date().strftime('%Y-%m-%d'))
    date_2 = np.datetime64(datetime.today(), 'D')
        
    return  [False, note, date_1, date_2]


