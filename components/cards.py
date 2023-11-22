# Imports
import time
import locale
from datetime import datetime
from dash import Input, Output, callback
from utils.data_manager import get_dataframe_2
from utils.data_manager import get_dataframe_main



@callback(Output("card-title-2", "children"),
              Input("date-picker-1", "value"))
def card_title_2(ano):
    value = f'Situação'
    return value


@callback(Output("card-title-3", "children"),
              Input("date-picker-1", "value"))
def card_title_3(ano):
    value = "Formas de pagamentos"
    return value


@callback(Output("card-title-4", "children"),
              Input("date-picker-1", "value"))
def card_title_4(ano):
    value = 'Extrato financeiro'
    return value


@callback(Output("card-title-5", "children"),
              Input("date-picker-1", "value"))
def card_title_5(ano):
    value = 'Contas utilizadas'
    return value


@callback(Output("card-title-6", "children"),
              Input("date-picker-1", "value"),)
def card_title_6(ano):
    value = 'Análise por fornecedor/cliente'
    return value


@callback(Output("card-title-8", "children"),
              Input("date-picker-1", "value"),)
def card_title_8(ano):
    value = 'Análise por categoria'
    return value


@callback(Output("card-title-9", "children"),
              Input("date-picker-1", "value"),)
def card_title_9(ano):
    value = 'Faturamento por período'
    return value


@callback(Output("card-title-10", "children"),
              Input("date-picker-1", "value"),)
def card_title_10(ano):
    value = 'Faturamento e taxa de variação'
    return value


@callback(Output("card-title-11", "children"),
              Input("date-picker-1", "value"),)
def card_title_11(ano):
    value = 'Despesas por período'
    return value


@callback(Output("card-title-12", "children"),
              Input("date-picker-1", "value"),)
def card_title_12(ano):
    value = 'Faturamento x despesas'
    return value


@callback(Output("card-title-13", "children"),
              Input("date-picker-1", "value"),)
def card_title_13(ano):
    value = 'Despesas por fornecedores e serviços (Pareto)'
    return value


@callback(Output("card-title-14", "children"),
              Input("date-picker-1", "value"),)
def card_title_14(ano):
    value = 'Faturamento e despesas'
    return value


@callback(Output("card-title-15", "children"),
              Input("date-picker-1", "value"),)
def card_title_15(ano):
    value = 'Faturamento por clientes e categoria'
    return value


@callback(Output("card-title-16", "children"),
              Input("date-picker-1", "value"),)
def card_title_16(ano):
    value = 'Análise por categorias (Pareto)'
    return value


@callback(Output("card-title-17", "children"),
              Input("date-picker-1", "value"),)
def card_title_17(ano):
    value = 'Faturamento por clientes (Pareto)'
    return value


@callback(Output("card-title-18", "children"),
              Input("date-picker-2", "value"),)
def card_title_18(data):
    date = datetime.strptime(data[0:10], '%Y-%m-%d')
    value = 'Faturamento - ' + date.strftime('%B %Y').capitalize()
    return value


@callback(Output("card-title-19", "children"),
              Input("date-picker-2", "value"),)
def card_title_19(final_date):
    date = datetime.strptime(final_date[0:10], '%Y-%m-%d')
    value = 'Despesas - ' + date.strftime('%B %Y').capitalize()
    return value


@callback(Output("card-title-20", "children"),
              [Input("date-picker-1", "value"),
               Input("date-picker-2", "value")])
def card_title_20(inicial_date, final_date):
    inicial_data = datetime.strptime(inicial_date[0:10], '%Y-%m-%d')
    final_data = datetime.strptime(final_date[0:10], '%Y-%m-%d')
    value = 'Distribuição faturamento | despesas - ' + inicial_data.strftime(
        '%B %Y').capitalize() + ' a ' + final_data.strftime('%B %Y').capitalize()
    return value


@callback(Output("card-title-21", "children"),
              Input("date-picker-1", "value"),)
def card_title_21(ano):
    #0ms
    value = 'Contas atrasadas por categoria'
    return value


@callback(Output("card-title-22", "children"),
              Input("date-picker-1", "value"),)
def card_title_22(ano):
    value = 'Detalhamento de atrasos'
    return value
#
#
#
#
#
# ---------- Card Values ---------- #
@callback(Output("card-text-1-2", "children"),
              Input("date-picker-2", "value"))
def card_val_1(final_date):

    df_1 = get_dataframe_main().copy()
    df_1 = df_1.loc[(df_1.data_movimento <= final_date)]
    data = df_1.saldo_conta_geral.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-2-2", "children"),
              Input("date-picker-2", "value"))
def card_val_2(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_bancobrasil.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-3-2", "children"),
              Input("date-picker-2", "value"))
def card_val_3(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_bradesco.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-4-2", "children"),
              Input("date-picker-2", "value"))
def card_val_4(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_nubank.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-5-2", "children"),
              Input("date-picker-2", "value"))
def card_val_5(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_btg.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-6-2", "children"),
              Input("date-picker-2", "value"))
def card_val_6(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_caixa.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-7-2", "children"),
              Input("date-picker-2", "value"))
def card_val_7(final_date):

    df_1 = get_dataframe_main().copy()
    data = df_1.saldo_conta_bancointer.values[-1]

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-8-2", "children"),
              [Input("date-picker-1", "value"),
              Input("date-picker-2", "value")])
def card_val_8(inicial_date, final_date):

    df_1 = get_dataframe_main().copy()

    df_1 = df_1.loc[(df_1.data_movimento >= inicial_date)
                    & (df_1.data_movimento <= final_date)]
    data = df_1.valor[(df_1.situacao == 'Atrasado') &
                      (df_1.operacao == 'Crédito')].sum()

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-9-2", "children"),
              [Input("date-picker-1", "value"),
              Input("date-picker-2", "value")])
def card_val_9(inicial_date, final_date):
    df_1 = get_dataframe_main().copy()

    df_1 = df_1.loc[(df_1.data_movimento >= inicial_date)
                    & (df_1.data_movimento <= final_date)]
    data = df_1.valor[(df_1.situacao == 'Atrasado') &
                      (df_1.operacao == 'Débito')].sum()

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-10-2", "children"),
              Input("date-picker-2", "value"))
def card_val_10(final_date):
    df_1 = get_dataframe_main().copy()

    df_1 = df_1.loc[(df_1.data_movimento <= final_date)]
    data = df_1.valor[(df_1.situacao == 'Em aberto') &
                      (df_1.operacao == 'Crédito')].sum()

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-11-2", "children"),
              Input("date-picker-2", "value"))
def card_val_11(final_date):
    df_1 = get_dataframe_main().copy()

    df_1 = df_1.loc[(df_1.data_movimento <= final_date)]
    data = df_1.valor[(df_1.situacao == 'Em aberto') &
                      (df_1.operacao == 'Débito')].sum()

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value


@callback(Output("card-text-12-2", "children"),
              [Input("date-picker-1", "value"),
               Input("date-picker-2", "value")])
def card_val_12(inicial_date, final_date):
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]
    df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
    df_4['months_mean'] = df_4.valor_original.mean()

    data = df_4.valor_original.sum()

    if data is not None:
        value = locale.currency(
            round(data, 2), grouping=True)
    else:
        value = locale.currency(
            round(0, 2), grouping=True)
    return value
#