# Imports
import pandas as pd
import os
from settings import *
from dash import Input, Output, callback

pd.options.mode.copy_on_write = True


# ---------- Dataframe main ---------- #
def get_dataframe_main():
    global df_main, file_timestamp

    local_timestamp = os.path.getmtime(dataset_path)

    if local_timestamp > file_timestamp:
        df_main = pd.read_csv(dataset_path,
                              index_col=[0],
                              encoding='utf8',
                              parse_dates=['data_movimento',
                                           'data_competencia',
                                           'data_original_vencimento',
                                           'data_prevista'], engine='c')
        file_timestamp = local_timestamp
    return df_main


# ---------- Dataframe 2 ---------- #
def get_dataframe_2(inicial_date, final_date):
    
    df_1 = get_dataframe_main().copy()
    df_1.sort_values(['data_competencia'], ascending=True, inplace=True)
    df_1.sort_index(ascending=True, inplace=True)
    df_2 = df_1.loc[(df_1.data_competencia >= inicial_date)
                    & (df_1.data_competencia <= final_date)]
    df_2['dia'] = df_2['data_competencia'].dt.day
    df_2['dia_mes_ano'] = df_2['data_competencia'].dt.strftime(
        '%d %b-%y').str.title()
    df_2['mes_ano'] = pd.to_datetime(df_2['data_competencia']).dt.strftime(
        '%b-%y').apply(lambda x: x.capitalize())
    df_2['ano'] = df_2['data_competencia'].dt.year
    df_2['mes_num'] = df_2['data_competencia'].dt.month
    df_2['trimestre'] = pd.to_datetime(
        df_2['data_competencia']).dt.to_period('Q').dt.strftime('T%q')
    df_2['trimestre_ano'] = pd.to_datetime(
        df_2['data_competencia']).dt.to_period('Q').dt.strftime('T%q-%y')
    
    return df_2


# ---------- Dataframe 1 dcc.Store ---------- #
@callback(Output("data-store-1", "data"),
              [Input('chart-1-px', 'selectedData'),
               Input('radioitem-1', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value'),
               Input('dropdown-8', 'value'),
               Input('radioitem-13', 'value')])
def get_dataframe_1(click_bar, radioitem_update, inicial_date, final_date, conta, oper):

    global radioitem_var, radioitem_var_oper, conta_var, inicial_date_var_2, final_date_var_2
    if (radioitem_update != radioitem_var) | (oper != radioitem_var_oper) | \
            (conta != conta_var) | (inicial_date != inicial_date_var_2) | (final_date != final_date_var_2):

        conta_var = conta
        radioitem_var = radioitem_update
        radioitem_var_oper = oper
        inicial_date_var_2 = inicial_date
        final_date_var_2 = final_date
        click_bar = None
        
    df = get_dataframe_main().copy()
    
    df_1 = df.loc[(df.data_movimento >= inicial_date)
                  & (df.data_movimento <= final_date)]
    df_1.sort_index(ascending=True, inplace=True)

    if oper == 'Crédito':
        df_1 = df_1[df_1.operacao == 'Crédito']
    elif oper == 'Débito':
        df_1 = df_1[df_1.operacao == 'Débito']

    if conta == 'Caixa':
        df_1 = df_1[df_1.conta_bancaria == 'Caixa']
        df_1['saldo_conta'] = df_1['saldo_conta_caixa']
    elif conta == 'Bradesco':
        df_1 = df_1[df_1.conta_bancaria == 'Bradesco']
        df_1['saldo_conta'] = df_1['saldo_conta_bradesco']
    elif conta == 'Nubank':
        df_1 = df_1[df_1.conta_bancaria == 'Nubank']
        df_1['saldo_conta'] = df_1['saldo_conta_nubank']
    elif conta == 'Banco Brasil':
        df_1 = df_1[df_1.conta_bancaria == 'Banco Brasil']
        df_1['saldo_conta'] = df_1['saldo_conta_bancobrasil']
    elif conta == 'BTG':
        df_1 = df_1[df_1.conta_bancaria == 'BTG']
        df_1['saldo_conta'] = df_1['saldo_conta_btg']
    elif conta == 'Banco Inter':
        df_1 = df_1[df_1.conta_bancaria == 'Banco Inter']
        df_1['saldo_conta'] = df_1['saldo_conta_bancointer']
    else:
        df_1['saldo_conta'] = df_1['saldo_conta_geral']

    if click_bar is not None:
        df_2 = pd.DataFrame(columns=df_1.columns)
        try:

            for i in range(len(click_bar['points'])):
                date = click_bar['points'][i]['customdata'][0]
                ano = click_bar['points'][i]['customdata'][1]
                oper = 'Crédito' if click_bar['points'][i]['customdata'][2] > 0 else 'Débito'
                situacao = click_bar['points'][i]['customdata'][3]

                df_ = df_1.loc[((df_1.dia_mes == date) |
                                (df_1.semana_name == date) |
                                (df_1.trimestre == date) |
                                (df_1.mes_name == date)) &
                               (df_1.ano == ano) &
                               (df_1.operacao == oper) &
                               (df_1.situacao == situacao)]

                df_2 = pd.concat([df_2, df_], ignore_index=True)

            df_2.sort_index(ascending=True, inplace=True)

            df_1 = df_2
            
        except:
            #import sys
            #raise sys.exc_info()[0]
            pass
    
    
    df_1['timestamp'] = df_1['timestamp'].astype('int64')

    return df_1.to_json(date_format='iso', orient='table')