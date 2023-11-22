# Imports
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
from plotly.subplots import make_subplots
from utils.theme_switch import ThemeSwitch
from utils.data_manager import *
from utils.functions import *
from settings import *

pd.options.mode.copy_on_write = True


@callback([Output('chart-1-px', 'figure'),
               Output('chart-1-px', 'style')],
              [Input('radioitem-1', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value'),
               Input('dropdown-8', 'value'),
               Input('radioitem-13', 'value'),
               Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               ],)
def chart_1_px(modo, incial_date, final_date, conta, oper, theme):
 
    df = get_dataframe_main().copy()
    
    df_1 = df.loc[(df.data_movimento >= incial_date)
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

    if modo == 'Dia' and not df_1.empty:

        # Df Bar
        df_2 = df_1.groupby(['situacao', 'mes_num', 'dia_mes', 'dia', 'ano', 'dia_mes_ano', 'operacao'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'dia'],
                         ascending=True, inplace=True)

        # Parâmetros Dia
        width_bar = 0.3 if len(df_2.dia_mes_ano.unique()) == 1 else 0.5 if len(df_2.dia_mes_ano.unique()) == 2 else 0.8
        var_x_bar = df_2.dia_mes_ano
        customdata_var = ['dia_mes', 'ano', 'valor_original', 'situacao']

        df_6 = df_1[['data_movimento', 'situacao_nova',
                     'conta_bancaria', 'dia_mes_ano', 'saldo_conta']]
        df_6.set_index('data_movimento', inplace=True)
        df_7 = df_6.groupby(pd.Grouper(freq='D')).last()
        df_7.dropna(inplace=True)
        var_x_line_saldo = df_7.dia_mes_ano

    elif modo == 'Semana' and not df_1.empty:

        # Df Bar
        df_2 = df_1.groupby(['situacao', 'mes_num', 'semana_name', 'semana', 'ano',
                             'semana_mes_ano', 'operacao'], as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'semana'],
                         ascending=True, inplace=True)

        # Parâmetros Semana
        width_bar = 0.3 if len(df_2.semana.unique()) == 1 else 0.5
        var_x_bar = df_2.semana_mes_ano
        customdata_var = ['semana_name', 'ano',
                          'valor_original', 'situacao']

        df_6 = df_1[['data_movimento', 'situacao_nova',
                     'conta_bancaria', 'semana_mes_ano', 'saldo_conta']]
        df_6.set_index('data_movimento', inplace=True)
        df_7 = df_6.groupby(pd.Grouper(freq='W')).last()
        df_7.dropna(inplace=True)
        var_x_line_saldo = df_7.semana_mes_ano

    elif modo == 'Mês' and not df_1.empty:

        # Df Bar
        df_2 = df_1.groupby(['situacao', 'mes_name', 'ano', 'mes_num', 'mes_ano', 'operacao'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)

        # Parâmetros Mês
        width_bar = 0.3 if len(df_2.mes_num.unique()) == 1 else 0.5 
        var_x_bar = df_2.mes_ano
        customdata_var = ['mes_name', 'ano', 'valor_original', 'situacao']

        df_6 = df_1[['data_movimento', 'situacao_nova',
                     'conta_bancaria', 'mes_ano', 'saldo_conta']]
        df_6.set_index('data_movimento', inplace=True)
        df_7 = df_6.groupby(pd.Grouper(freq='M')).last()
        df_7.dropna(inplace=True)
        var_x_line_saldo = df_7.mes_ano

    elif modo == 'Trimestre' and not df_1.empty:

        # Df Bar
        df_2 = df_1.groupby(['situacao', 'trimestre', 'ano', 'trimestre_ano', 'operacao'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)

        # Parâmetros Trimestre
        width_bar = 0.3 if len(df_2.trimestre.unique()) == 1 else 0.5 
        var_x_bar = df_2.trimestre_ano
        customdata_var = ['trimestre', 'ano',
                          'valor_original', 'situacao']

        df_6 = df_1[['data_movimento', 'situacao_nova',
                     'conta_bancaria', 'trimestre_ano', 'saldo_conta']]
        df_6.set_index('data_movimento', inplace=True)
        df_7 = df_6.groupby(pd.Grouper(freq='Q')).last()
        df_7.dropna(inplace=True)
        var_x_line_saldo = df_7.trimestre_ano

    if not df_1.empty:
        fig = go.Figure()
        fig.add_trace(px.bar(df_2,
                             y=df_2.valor_original,
                             x=var_x_bar,
                             orientation='v',
                             barmode='relative',
                             custom_data=customdata_var,
                             ).data[0])

        color_var = np.where((df_2.valor_original > 0) & (df_2.situacao == 'Quitado'), '#43aa8b',
                             np.where((df_2.valor_original < 0) & (df_2.situacao == 'Quitado'), '#f94144',
                                      np.where((df_2.valor_original != 0) & (df_2.situacao == 'Atrasado'), 'rgba(243,114,44, 0.6)',
                                               np.where((df_2.valor_original != 0) & (df_2.situacao == 'Conciliado'), 'rgba(249,199,79, 0.6)',
                                                        np.where((df_2.valor_original < 0) & (df_2.situacao == 'Em aberto'), 'rgba(249, 65, 68, 0.4)', 'rgba(67, 170, 139, 0.4)')))))

        fig.update_traces(marker_color=color_var, width=width_bar)
        
        #fig.update_traces(width=[0.2 if len(fig.data[0]['x']) == 4 else 0.8])
        fig.update_traces(hovertemplate=' %{customdata[0]} - %{customdata[1]}<extra></extra><br>'
                          ' R$ %{customdata[2]:,.2f} (%{customdata[3]})')

        fig.add_trace(go.Scatter(
            x=var_x_line_saldo,
            y=df_7.saldo_conta,
            mode='lines',
            showlegend=False,
            fillcolor='rgba(87, 117, 144, 0.1)',
            fill='tozeroy',
            line_shape='spline',
            line_smoothing=0.8,  # smoothing  0 ~ 1.3
            customdata=np.stack(
                (df_7.situacao_nova, df_7.conta_bancaria), axis=-1),
            line=dict(width=2, color='#577590'),
            hovertemplate=' %{x}<extra></extra> <br> R$ %{y:,.2f} (%{customdata[0]})',
            ))

        fig.update_layout(
            autosize=True,
            separators=',.',
            margin=fig_margin,
            height=None,
            width=None,
            #hoverlabel = dict(font=dict(color='white')),
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            bargap=1,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            #xaxis={'categoryorder': 'total ascending'}
            #hovermode="y unified",
            #template='flatly' if theme else 'darkly',
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',
                         zeroline=True, zerolinewidth=1, zerolinecolor='black')
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, gridcolor='#E0E0E0',)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
        

        """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark,)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return  [fig, {'visibility': 'visible'}]


@callback([Output('chart-2-px', 'figure'),
               Output('chart-2-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-3', 'value'),
               Input('data-store-1', 'data')])
def chart_2_px(theme, contas, data_store):
    
    df_1 = pd.read_json(data_store, orient='table')

    if contas == 'Débito':
        df_2 = df_1[df_1.operacao == 'Débito']

    elif contas == 'Crédito':
        df_2 = df_1[df_1.operacao == 'Crédito']

    if not df_2.empty:

        fig = px.pie(df_2,
                     names='situacao',
                     # values='valor_original',
                     # color_discrete_sequence=px.colors.qualitative.Pastel,
                     color='situacao',
                     color_discrete_map={'Atrasado': '#f3722c', 'Quitado': '#90be6d',
                                         'Conciliado': '#f9c74f', 'Em aberto': '#577590'},
                     hole=0.5,
                     template=theme_light if theme else theme_dark,)

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            height=None,
            width=None,
            separators=',.',
            showlegend=False,
            legend_title=None,
            # clickmode='event+select',
            # legend=dict(orientation="h", yanchor="bottom", y=-0.2,
            # xanchor="center", x=0.5, font=dict(size=12)),
            modebar=mode_bar,
            template=theme_light if theme else theme_dark,
        )

        #fig.update_traces(hovertemplate='%{label} - %{value}')
        fig.update_traces(textposition='outside', textinfo='percent+label',
                          hovertemplate=' %{label} - %{value}',
                          marker=dict(line=dict(color='white', width=2)))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark,)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-3-px', 'figure'),
               Output('chart-3-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-4', 'value'),
               Input('data-store-1', 'data')])
def chart_3_px(theme, contas, data_store):
    
    df_1 = pd.read_json(data_store, orient='table')

    if contas == 'Débito':
        df_2 = df_1[df_1.operacao == 'Débito']

    elif contas == 'Crédito':
        df_2 = df_1[df_1.operacao == 'Crédito']

    df_3 = df_2.groupby(['forma_pgto_recbto']
                        ).size().reset_index(name='Contagem')

    if not df_3.empty:

        fig = px.bar(df_3,
                     y='forma_pgto_recbto',
                     x='Contagem',
                     orientation='h',
                     custom_data=['forma_pgto_recbto'],
                     color_discrete_sequence=['#277da1'],
                     template=theme_light if theme else theme_dark,)

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            yaxis_title=None,
            xaxis_title=None,
            separators=',.',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            # hovermode="x unified",
            template=theme_light if theme else theme_dark,
        )

        fig.update_traces(width=0.3 if len(df_3) == 1 else None)
        fig.update_yaxes(showgrid=False, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12))
        fig.update_xaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        #fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        fig.update_traces(
            hovertemplate=' %{customdata[0]}<extra></extra> - %{x} ')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-4-px', 'children'),
               Output('chart-4-px', 'style')],
              [Input('data-store-1', 'data'),
               Input(ThemeSwitch.ids.switch('theme-2'), 'checked')])
def chart_4_px(data_store, theme):
    
    if theme:
        header_color = '#787878'
        bg_color_odd = 'rgb(248, 248, 248)'
        bg_color_even = '#E8E8E8'
    else:
        header_color = '#585858'
        bg_color_odd = 'rgb(32, 32, 32)'
        bg_color_even = '#444444'

    df_1 = pd.read_json(data_store, orient='table')

    if not df_1.empty:

        conditional_style = [
            {
                'if': {
                    'column_id': 'Descrição'
                },
                'width': '500px'
            },
            {
                'if': {
                    'column_id': 'Categoria 1'
                },
                'width': '350px'
            },
            {
                'if': {
                    'column_id': 'Nome do fornecedor/cliente'
                },
                'width': '250px'
            },
            {
                'if': {
                    'column_id': 'Situação',
                    'filter_query': '{Situação} = "Quitado"'
                },
                'color': '#90be6d',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Situação',
                    'filter_query': '{Situação} = "Em aberto"'
                },
                'color': '#577590',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Situação',
                    'filter_query': '{Situação} = "Atrasado"'
                },
                'color': '#f3722c',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Situação',
                    'filter_query': '{Situação} = "Conciliado"'
                },
                'color': '#f9c74f',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Tipo da operação',
                    'filter_query': '{Tipo da operação} = "Débito"'
                },
                'color': '#f94144',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Valor original (R$)',
                    'filter_query': '{Valor original (R$)} < 0'
                },
                'color': '#f94144',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Valor original (R$)',
                    'filter_query': '{Valor original (R$)} > 0'
                },
                'color': '#43aa8b',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'Tipo da operação',
                    'filter_query': '{Tipo da operação} = "Crédito"'
                },
                'color': '#43aa8b',
                'fontWeight': 'bold',

            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': bg_color_odd
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': bg_color_even
            }
        ]

        df_1 = df_1.rename(columns={'data_movimento': 'Data movimento',
                                    'fornecedor_cliente': 'Nome do fornecedor/cliente',
                                    'operacao': 'Tipo da operação',
                                    'descricao': 'Descrição',
                                    'conta_bancaria': 'Conta bancária',
                                    'forma_pgto_recbto': 'Forma de pgto/recbto',
                                    'valor': 'Valor (R$)',
                                    'saldo_conta': 'Saldo conta (R$)',
                                    'situacao': 'Situação',
                                    'valor_original': 'Valor original',
                                    'data_competencia': 'Data de competência',
                                    'data_original_vencimento': 'Data de vencimento',
                                    'data_prevista': 'Data prevista',
                                    'categoria': 'Categorias',
                                    'centro_custo': 'Centro de Custo',

                                    })

        df_1 = df_1.iloc[:, 0:13]

        df_1['Data movimento'] = df_1['Data movimento'].dt.strftime('%d-%m-%Y')
        df_1['Data de competência'] = df_1['Data de competência'].dt.strftime(
            '%d-%m-%Y')
        df_1['Data de vencimento'] = df_1['Data de vencimento'].dt.strftime(
            '%d-%m-%Y')
        df_1['Data prevista'] = df_1['Data prevista'].dt.strftime('%d-%m-%Y')

        table = dash_table.DataTable(
            data=df_1.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_1.columns],
            page_size=100,
            # row_selectable="single",
            style_data_conditional=conditional_style,
            fixed_rows={'headers': True, 'data': 0},
            export_format='xlsx',
            export_headers='display',
            # row_selectable="multi",
            # virtualization=True,  # Causa problemas de atualização na mudança de abas
            sort_action='native',
            # editable=True,
            # filter_action='native',
            style_header={'fontWeight': 'bold',
                          'textAlign': 'center',
                          # 'whiteSpace': 'nowrap',
                          'backgroundColor': header_color,
                          'color': 'white',
                          'fontSize': 15,
                          'height': '40px',
                          'margin': '10px',
                          },
            style_table={
                # 'overflowY': 'auto',
                # 'overflowX': 'scroll',
                'height': '280px',
                'width': '100%',
                'margin': '0px',
                # 'margin-right': '50px'
            },
            style_cell={'textAlign': 'left',
                        'fontSize': 13,
                        'margin': '10px',
                        'minWidth': '200px',
                        },

        )

    else:
        table = None
    return [table, {'visibility': 'visible'}]


@callback([Output('chart-5-px', 'figure'),
               Output('chart-5-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('data-store-1', 'data')])
def chart_5_px(theme, data_store):
    
    df_1 = pd.read_json(data_store, orient='table')

    df_2 = df_1.groupby(['conta_bancaria']
                        ).size().reset_index(name='Contagem')

    if not df_2.empty:

        fig = px.bar(df_2,
                     y='conta_bancaria',
                     x='Contagem',
                     orientation='h',
                     custom_data=['conta_bancaria'],
                     color_discrete_sequence=['#f3722c'],
                     template=theme_light if theme else theme_dark,)

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            # hovermode="x unified",
            template=theme_light if theme else theme_dark,
        )

        fig.update_traces(width=0.3 if len(df_2) == 1 else None)
        fig.update_yaxes(showgrid=False, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12))
        fig.update_xaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        #fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        fig.update_traces(
            hovertemplate=' %{customdata[0]}<extra></extra><br> Qtd - %{x} ')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-6-px', 'figure'),
               Output('chart-6-px', 'style'),],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('dropdown-5', 'value'),
               Input('radioitem-6', 'value'),
               Input('data-store-1', 'data'),
               Input('radioitem-1', 'value')])
def chart_6_px(theme, client_fornec, contas, data_store, periodo):
    
    df_1 = pd.read_json(data_store, orient='table')

    df_1 = df_1.loc[(df_1.operacao == contas) & (
        df_1.fornecedor_cliente == client_fornec)]

    if periodo == 'Dia':
        df_2 = df_1.groupby(['situacao', 'mes_num', 'dia_mes', 'dia', 'ano', 'dia_mes_ano'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'dia'],
                         ascending=True, inplace=True)
        x_bar = df_2['dia_mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.dia_mes_ano.unique()) == 1 else 0.7 if len(
            df_2.dia_mes_ano.unique()) == 2 else None

    elif periodo == 'Semana':
        df_2 = df_1.groupby(['dia_mes_ano', 'situacao', 'mes_num', 'semana_name', 'semana', 'ano',
                             'semana_mes_ano'], as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'semana'],
                         ascending=True, inplace=True)
        x_bar = df_2['semana_mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.semana.unique()) == 1 else 0.7 if len(
            df_2.semana.unique()) == 2 else None

    elif periodo == 'Mês':
        df_2 = df_1.groupby(['dia_mes_ano', 'mes_num', 'situacao', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
        x_bar = df_2['mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.mes_num.unique()) == 1 else 0.7 if len(
            df_2.mes_num.unique()) == 2 else None

    else:
        df_2 = df_1.groupby(['dia_mes_ano', 'situacao', 'trimestre', 'ano', 'trimestre_ano'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)
        x_bar = df_2['trimestre_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.trimestre.unique()) == 1 else 0.7 if len(
            df_2.trimestre.unique()) == 2 else None

    if not df_2.empty:
        
        if contas == 'Débito':
            df_2['valor_original'] = df_2.valor_original * -1

        fig = px.bar(df_2,
                     y='valor_original',
                     x=x_bar,
                     color='situacao',
                     orientation='v',
                     custom_data=customdata_var,
                     color_discrete_map={'Atrasado': '#f3722c', 'Quitado': '#90be6d',
                                         'Conciliado': '#f9c74f', 'Em aberto': '#577590'},
                     template=theme_light if theme else theme_dark,)
        

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            # hovermode="x unified"
        )
        
        fig.update_traces(width=width_var)
        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12),
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=True)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        if contas == 'Débito':
            fig.update_traces(
                hovertemplate=' %{customdata[1]}<extra></extra><br> Débito: R$ %{y:,.2f}')
        if contas == 'Crédito':
            fig.update_traces(
                hovertemplate=' %{customdata[1]}<extra></extra><br> Crédito: R$ %{y:,.2f}')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-8-px', 'figure'),
               Output('chart-8-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('dropdown-6', 'value'),
               Input('radioitem-5', 'value'),
               Input('data-store-1', 'data'),
               Input('radioitem-1', 'value')])
def chart_8_px(theme, categoria, contas, data_store, periodo):
    
    df_1 = pd.read_json(data_store, orient='table')

    df_1 = df_1.loc[(df_1.operacao == contas) & (
        df_1.categoria_nova == categoria)]

    if periodo == 'Dia':
        df_2 = df_1.groupby(['situacao', 'mes_num', 'dia_mes', 'dia', 'ano', 'dia_mes_ano'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'dia'],
                         ascending=True, inplace=True)
        x_bar = df_2['dia_mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.dia_mes_ano.unique()) == 1 else 0.7 if len(
            df_2.dia_mes_ano.unique()) == 2 else None

    elif periodo == 'Semana':
        df_2 = df_1.groupby(['dia_mes_ano', 'situacao', 'mes_num', 'semana_name', 'semana', 'ano',
                             'semana_mes_ano'], as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num', 'semana'],
                         ascending=True, inplace=True)
        x_bar = df_2['semana_mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.semana.unique()) == 1 else 0.7 if len(
            df_2.semana.unique()) == 2 else None


    elif periodo == 'Mês':
        df_2 = df_1.groupby(['dia_mes_ano', 'mes_num', 'situacao', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_2.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
        x_bar = df_2['mes_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.mes_num.unique()) == 1 else 0.7 if len(
            df_2.mes_num.unique()) == 2 else None

    else:
        df_2 = df_1.groupby(['dia_mes_ano', 'situacao', 'trimestre', 'ano', 'trimestre_ano'],
                            as_index=False)['valor_original'].sum()
        df_2.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)
        x_bar = df_2['trimestre_ano']
        customdata_var = ['valor_original', 'dia_mes_ano']
        width_var = 0.3 if len(df_2.trimestre.unique()) == 1 else 0.7 if len(
            df_2.trimestre.unique()) == 2 else None

    if not df_2.empty:

        if contas == 'Débito':
            df_2['valor_original'] = df_2.valor_original * -1

        fig = px.bar(df_2,
                     y='valor_original',
                     x=x_bar,
                     color='situacao',
                     orientation='v',
                     custom_data=customdata_var,
                     color_discrete_map={'Atrasado': '#f3722c', 'Quitado': '#90be6d',
                                         'Conciliado': '#f9c74f', 'Em aberto': '#577590'},
                     template=theme_light if theme else theme_dark,)

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            # hovermode="x unified"
            template=theme_light if theme else theme_dark,
        )
        
        fig.update_traces(width=width_var)
        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12),
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=True)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        if contas == 'Débito':
            fig.update_traces(
                hovertemplate=' %{customdata[1]}<extra></extra><br> Débito: R$ %{y:,.2f}')
        if contas == 'Crédito':
            fig.update_traces(
                hovertemplate=' %{customdata[1]}<extra></extra><br> Crédito: R$ %{y:,.2f}')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-9-px', 'figure'),
               Output('chart-9-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-7', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_9_px(theme, periodo, inicial_date, final_date):
           
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]

    if periodo == 'Mês':
        df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
        df_4['mean_value'] = df_4.valor_original.mean()
        x_bar_var = df_4.mes_ano
        x_line_var = df_4.mes_ano

    else:
        df_4 = df_3.groupby(['trimestre', 'ano', 'trimestre_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)
        df_4['mean_value'] = df_4.valor_original.mean()
        x_bar_var = df_4.trimestre_ano
        x_line_var = df_4.trimestre_ano

    if not df_4.empty:
        fig = go.Figure()
        fig.add_trace(px.bar(df_4,
                             y='valor_original',
                             x=x_bar_var,
                             orientation='v',
                             text_auto='.2s',
                             color_discrete_sequence=['#43aa8b'],
                             template=theme_light if theme else theme_dark).data[0])
        fig.update_traces(width=[0.3 if len(fig.data[0]['x']) == 1 else 0.8])
        fig.update_traces(hovertemplate=' R$ %{y:,.2f}')
        fig.update_traces(texttemplate='<b> %{y:.3s}   </b>', textposition='inside',
                          textangle=270, textfont=dict(color='white', size=11, family='Arial'))
        """fig.update_traces(texttemplate='<b> %{text:,.2f}  </b>', textposition='inside',
                          textangle=270, textfont=dict(color='white', size=10, family='Arial'))"""

        fig.add_trace(go.Scatter(x=x_line_var,
                                 y=df_4.mean_value,
                                 mode='lines',
                                 showlegend=False,
                                 line=dict(width=3, color='#f9c74f',
                                           dash='dash'),
                                 hovertemplate=' Faturamento médio: R$ %{y:,.2f}<extra></extra>'
                                 ))

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
            
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12),
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=True)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""

    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-10-px', 'figure'),
               Output('chart-10-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-8', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_10_px(theme, periodo, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]

    if periodo == 'Mês':
        df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)

        x_bar_var = df_4.mes_ano
        x_line_var = df_4.mes_ano

    else:
        df_4 = df_3.groupby(['trimestre', 'ano', 'trimestre_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)

        x_bar_var = df_4.trimestre_ano
        x_line_var = df_4.trimestre_ano

    df_4['returns'] = df_4.valor_original.pct_change()
    # df_4.dropna(inplace=True)
    df_4.fillna(0, inplace=True)
    df_4['returns_pct'] = round(df_4.returns * 100, 2)
    df_4['mean_value'] = df_4.valor_original.mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not df_4.empty:

        # Plot - 1
        fig_bar = px.bar(df_4,
                         y='returns_pct',
                         x=x_bar_var,
                         orientation='v',
                         barmode='relative',
                         template=theme_light if theme else theme_dark,)
        fig_bar.update_traces(
            width=[0.2 if len(fig_bar.data[0]['x']) == 1 else 0.8])
        fig_bar.update_traces(hovertemplate=' %{y}%<extra></extra>')
        fig_bar.update_traces(marker_color=np.where(
            df_4['returns_pct'].values < 0, '#f3722c', '#577590'))

        # Plot - 2
        fig_line = px.line(df_4,
                           y='valor_original',
                           x=x_line_var,
                           markers=False,
                           template=theme_light if theme else theme_dark,)
        fig_line.update_traces(
            hovertemplate=' R$ %{y:,.2f}<extra></extra>')
        fig_line.update_traces(yaxis="y2", line=dict(
            width=5, dash=None, color='#90be6d'),)

        fig.add_traces(fig_bar.data + fig_line.data)
        # fig.layout.yaxis2.type="log"

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title="Taxa (%)",
            yaxis2_title="Faturamento (R$)",
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=False, gridwidth=gridwidth, visible=True,
                         zeroline=True, zerolinewidth=1, zerolinecolor='black', secondary_y=False,
                         title=dict(standoff=2))
        fig.update_yaxes(range=[0, max(df_4.valor_original) + 10000], showgrid=True, gridwidth=gridwidth,
                         secondary_y=True, gridcolor='#E0E0E0' if theme else '#484848',)
        #fig.update_xaxes(showgrid=True, gridwidth=gridwidth)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-11-px', 'figure'),
               Output('chart-11-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-9', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_11_px(theme, periodo, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_2['valor_original'] = df_2.valor_original * -1
    df_3 = df_2.loc[(df_2.operacao == 'Débito') & (
        df_2.despesas_faturamento == 'despesas')]

    if periodo == 'Mês':
        df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
        df_4['mean_value'] = df_4.valor_original.mean()
        x_bar_var = df_4.mes_ano
        x_line_var = df_4.mes_ano

    else:
        df_4 = df_3.groupby(['trimestre', 'ano', 'trimestre_ano'], as_index=False)[
            'valor_original'].sum()
        df_4.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)
        df_4['mean_value'] = df_4.valor_original.mean()
        x_bar_var = df_4.trimestre_ano
        x_line_var = df_4.trimestre_ano

    if not df_4.empty:
        fig = go.Figure()
        fig.add_trace(px.bar(df_4,
                             y='valor_original',
                             x=x_bar_var,
                             orientation='v',
                             text_auto='.2s',
                             color_discrete_sequence=['#f94144'],
                             template=theme_light if theme else theme_dark,).data[0])
        fig.update_traces(width=[0.3 if len(fig.data[0]['x']) == 1 else 0.8])
        fig.update_traces(hovertemplate=' R$ %{y:,.2f}')
        fig.update_traces(texttemplate='<b> %{y:.3s}   </b>', textposition='inside',
                          textangle=270, textfont=dict(color='white', size=11, family='Arial'))
        """fig.update_traces(texttemplate='<b> %{text:,.2f}  </b>', textposition='inside',
                          textangle=270, textfont=dict(color='white', size=10, family='Arial'))"""

        fig.add_trace(go.Scatter(x=x_line_var,
                                 y=df_4.mean_value,
                                 mode='lines',
                                 showlegend=False,
                                 line=dict(width=3, color='#f9c74f',
                                           dash='dash'),
                                 hovertemplate=' Despesa média: R$ %{y:,.2f}<extra></extra>'
                                 ))

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            yaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         visible=True, tickfont=dict(size=12),
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=True)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-12-px', 'figure'),
               Output('chart-12-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-10', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_12_px(theme, periodo, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    # Dataset - Faturamento
    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]
    df_fatura = df_3

    # Dataset - Despesas
    df_4 = df_2.loc[(df_2.operacao == 'Débito') & (
        df_2.despesas_faturamento == 'despesas')]
    df_4['valor_original'] = df_4.valor_original * -1
    df_despesa = df_4

    if periodo == 'Mês':
        df_5 = df_fatura.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_5.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)

        df_6 = df_despesa.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
            'valor_original'].sum()
        df_6.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)

        df_7 = pd.merge(df_5, df_6, on=[
                        'mes_ano', 'mes_num', 'ano'], how='outer', suffixes=('_fat', '_desp'))
        df_7.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
        df_7['lucro_estimado'] = df_7.valor_original_fat - \
            df_7.valor_original_desp
        df_7.dropna(inplace=True)
        x_bar_var = df_7.mes_ano

    else:
        df_5 = df_fatura.groupby(['trimestre', 'ano', 'trimestre_ano'], as_index=False)[
            'valor_original'].sum()
        df_5.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)

        df_6 = df_despesa.groupby(['trimestre', 'ano', 'trimestre_ano'], as_index=False)[
            'valor_original'].sum()
        df_6.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)

        df_7 = pd.merge(df_5, df_6, on=[
                        'trimestre', 'ano', 'trimestre_ano'], how='outer', suffixes=('_fat', '_desp'))
        df_7.sort_values(['ano', 'trimestre'], ascending=True, inplace=True)
        df_7['lucro_estimado'] = df_7.valor_original_fat - \
            df_7.valor_original_desp
        df_7.dropna(inplace=True)
        x_bar_var = df_7.trimestre_ano

    if not df_2.empty:
        fig = make_subplots(shared_yaxes=True)
        
        fig.add_bar(y=df_7.valor_original_fat,
                    x=x_bar_var,
                    # opacity=0.8,
                    width=0.5 if len(df_7.valor_original_fat) == 1 else 0.8,
                    #width=0.8,
                    name='Faturamento',
                    marker_color=['#43aa8b' for i in range(len(df_7))],
                    )

        fig.add_bar(y=df_7.valor_original_desp,
                    x=x_bar_var,
                    width=0.15 if len(df_7.valor_original_desp) == 1 else 0.4,
                    #width=0.4,
                    name='Despesas',
                    marker_color=['#f94144' for i in range(len(df_7))],
                    )

        fig.add_bar(y=df_7.lucro_estimado,
                    x=x_bar_var,
                    width=0.3 if len(df_7.lucro_estimado) == 1 else 0.6,
                    #width=0.6,
                    opacity=0.9,
                    name='Lucro líquido',
                    marker_color=['#277da1' for i in range(len(df_7))],
                    )
        
        fig.update_layout(
            barmode='overlay',
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            #yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            #xaxis={'categoryorder': 'total ascending'}
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        fig.update_traces(hovertemplate=' R$ %{y:,.2f}<extra></extra>')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-13-px', 'figure'),
               Output('chart-13-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_13_px(theme, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_5 = df_2.loc[(df_2.operacao == 'Débito') & (
        df_2.despesas_faturamento == 'despesas')]
    df_5['valor_original'] = df_5.valor_original * -1

    df_6 = df_5[['valor_original', 'fornecedor_cliente']]
    df_7 = df_6.groupby(['fornecedor_cliente'], as_index=False)[
        'valor_original'].sum()
    df_7 = df_7.sort_values('valor_original', ascending=False)
    df_7['porcentagem'] = round(
        (df_7['valor_original'] / df_7['valor_original'].sum()) * 100, 2)
    df_7['porcentagem_acumulada'] = df_7.porcentagem.cumsum()

    if not df_7.empty:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_bar = px.bar(df_7,
                         y='valor_original',
                         x='fornecedor_cliente',
                         orientation='v',
                         custom_data=['porcentagem_acumulada', 'porcentagem'],
                         color_discrete_sequence=['#577590'],
                         template=theme_light if theme else theme_dark,)
        fig_bar.update_traces(hovertemplate=' R$ %{y:,.2f}  (%{customdata[1]:,.2f}%)',
                              width=0.3 if len(df_7) == 1 else None)

        fig_line = px.line(df_7,
                           y='porcentagem_acumulada',
                           x='fornecedor_cliente',
                           markers=False,
                           template=theme_light if theme else theme_dark,)
        fig_line.update_traces(hovertemplate=' %{y:,.2f}%<extra></extra>')
        fig_line.update_traces(yaxis="y2", line=dict(
            width=5, dash=None, color='#f3722c'),)

        fig.add_traces(fig_bar.data + fig_line.data)

        fig.update_layout(
            autosize=True,
            yaxis_type='log',
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            xaxis_title=None,
            yaxis_title='Faturamento (R$)',
            yaxis2_title="Acumulado (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=False, gridwidth=gridwidth, visible=True,
                         zeroline=True, zerolinewidth=1, zerolinecolor='black', secondary_y=False,
                         title=dict(standoff=2))
        fig.update_yaxes(range=[0, max(df_7.porcentagem_acumulada) + 10],
                         showgrid=True, gridwidth=gridwidth, secondary_y=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=False)

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-14-px', 'figure'),
               Output('chart-14-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_14_px(theme, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)
    df_2 = df_2.loc[(df_2.despesas_faturamento == 'faturamento')
                    | (df_2.despesas_faturamento == 'despesas')]
    df_2 = df_2.groupby(['despesas_faturamento'], as_index=False)[
        'valor_original'].sum()
    df_2['valor_original'] = np.where(
        df_2.valor_original < 0, (df_2.valor_original * -1), df_2.valor_original)
    df_2['despesas_faturamento'] = df_2.despesas_faturamento.str.capitalize()
    #df_2.loc[len(df_2)] = ['Lucro', df_2.loc[1, 'valor_original'] - df_2.loc[0, 'valor_original']]

    if not df_2.empty:

        fig = px.pie(df_2,
                     values='valor_original',
                     color='despesas_faturamento',
                     color_discrete_map={'Faturamento': '#43aa8b',
                                         'Despesas': '#f94144', 'Lucro': '#577590'},
                     hole=0.5,
                     custom_data=['despesas_faturamento'],
                     template=theme_light if theme else theme_dark,)

        fig.update_layout(
            autosize=True,
            margin=fig_margin,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            height=None,
            width=None,
            separators=',.',
            showlegend=False,
            legend_title=None,
            # clickmode='event+select',
            # legend=dict(orientation="h", yanchor="bottom", y=-0.2,
            # xanchor="center", x=0.5, font=dict(size=12)),
            modebar=mode_bar,
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
        )

        #fig.update_traces(hovertemplate='%{label} - %{value}')
        fig.update_traces(textposition='outside', textinfo='percent+text',
                          hovertemplate='%{customdata[0]} - %{value}',
                          marker=dict(line=dict(color='white', width=2)))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-15-px', 'figure'),
               Output('chart-15-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_15_px(theme, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    df_5 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]

    df_6 = df_5[['valor_original', 'fornecedor_cliente', 'categoria_nova']]
    df_7 = df_6.groupby(['fornecedor_cliente', 'categoria_nova'], as_index=False)[
        'valor_original'].sum()
    df_7['porcentagem'] = round(
        (df_7['valor_original'] / df_7['valor_original'].sum()) * 100, 2)

    if not df_7.empty:

        fig = px.bar(df_7,
                     y='valor_original',
                     x='fornecedor_cliente',
                     orientation='v',
                     color='categoria_nova',
                     custom_data=['porcentagem'],
                     color_discrete_map={'Categoria 33': '#277da1',
                                         'Categoria 4': '#f3722c',
                                         'Categoria 7': '#90be6d'},
                     # color_discrete_sequence=['#577590'],
                     )
        fig.update_traces(hovertemplate=' R$ %{y:,.2f}  (%{customdata[0]}%)')

        fig.update_layout(
            autosize=True,
            yaxis_type='log',
            margin=fig_margin,
            height=None,
            width=None,
            showlegend=False,
            separators=',.',
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            template=theme_light if theme else theme_dark,
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         visible=False, tickfont=dict(size=12),
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=False)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-16-px', 'figure'),
               Output('chart-16-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('radioitem-12', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_16_px(theme, categoria, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    if categoria == 'Despesas':

        df_5 = df_2.loc[(df_2.operacao == 'Débito') & (
            df_2.despesas_faturamento == 'despesas')]
        df_5['valor_original'] = df_5.valor_original * -1
        var_1 = 'Despesas (R$)'

    else:
        df_5 = df_2.loc[(df_2.operacao == 'Crédito') & (
            df_2.despesas_faturamento == 'faturamento')]
        var_1 = 'Faturamento (R$)'

    df_6 = df_5[['valor_original', 'categoria_nova']]
    df_7 = df_6.groupby(['categoria_nova'], as_index=False)[
        'valor_original'].sum()
    df_7 = df_7.sort_values('valor_original', ascending=False)
    df_7['porcentagem'] = round(
        (df_7['valor_original'] / df_7['valor_original'].sum()) * 100, 2)
    df_7['porcentagem_acumulada'] = df_7.porcentagem.cumsum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not df_7.empty:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_bar = px.bar(df_7,
                         y='valor_original',
                         x='categoria_nova',
                         orientation='v',
                         custom_data=['porcentagem_acumulada', 'porcentagem'],
                         color_discrete_sequence=['#577590'],
                         template=theme_light if theme else theme_dark,)
        fig_bar.update_traces(hovertemplate=' R$ %{y:,.2f}  (%{customdata[1]:,.2f}%)',
                              width=0.3 if len(df_7) == 1 else None)

        fig_line = px.line(df_7,
                           y='porcentagem_acumulada',
                           x='categoria_nova',
                           markers=False,
                           template=theme_light if theme else theme_dark,)
        fig_line.update_traces(hovertemplate=' %{y:,.2f}%<extra></extra>')
        fig_line.update_traces(yaxis="y2", line=dict(
            width=5, dash=None, color='#f3722c'),)

        fig.add_traces(fig_bar.data + fig_line.data)

        fig.update_layout(
            autosize=True,
            yaxis_type='log',
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            xaxis_title=None,
            yaxis_title=var_1,
            yaxis2_title="Acumulado (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=False, gridwidth=gridwidth, visible=True,
                         zeroline=True, zerolinewidth=1, zerolinecolor='black',
                         secondary_y=False, title=dict(standoff=2))
        fig.update_yaxes(range=[0, max(df_7.porcentagem_acumulada) + 10],
                         showgrid=True, gridwidth=gridwidth, secondary_y=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=False)

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-17-px', 'figure'),
               Output('chart-17-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_17_px(theme, inicial_data, final_data):
    
    df_2 = get_dataframe_2(inicial_data, final_data)

    df_5 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]

    df_6 = df_5[['valor_original', 'fornecedor_cliente']]
    df_7 = df_6.groupby(['fornecedor_cliente'], as_index=False)[
        'valor_original'].sum()
    df_7 = df_7.sort_values('valor_original', ascending=False)
    df_7['porcentagem'] = round(
        (df_7['valor_original'] / df_7['valor_original'].sum()) * 100, 2)
    df_7['porcentagem_acumulada'] = df_7.porcentagem.cumsum()

    if not df_7.empty:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig_bar = px.bar(df_7,
                         y='valor_original',
                         x='fornecedor_cliente',
                         orientation='v',
                         custom_data=['porcentagem_acumulada', 'porcentagem'],
                         color_discrete_sequence=['#577590'],
                         template=theme_light if theme else theme_dark,)
        fig_bar.update_traces(hovertemplate=' R$ %{y:,.2f}  (%{customdata[1]:,.2f}%)',
                              width=0.3 if len(df_7) == 1 else None)

        fig_line = px.line(df_7,
                           y='porcentagem_acumulada',
                           x='fornecedor_cliente',
                           markers=False,
                           template=theme_light if theme else theme_dark,)
        fig_line.update_traces(hovertemplate=' %{y:,.2f}%<extra></extra>')
        fig_line.update_traces(yaxis="y2", line=dict(
            width=5, dash=None, color='#f3722c'),)

        fig.add_traces(fig_bar.data + fig_line.data)

        fig.update_layout(
            autosize=True,
            yaxis_type='log',
            margin=fig_margin,
            height=None,
            width=None,
            separators=',.',
            xaxis_title=None,
            yaxis_title='Faturamento (R$)',
            yaxis2_title="Acumulado (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            #xaxis={'categoryorder': 'total ascending'},
            modebar=mode_bar,
            # yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            # barmode="stack",
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=False, gridwidth=gridwidth, visible=True,
                         zeroline=True, zerolinewidth=1, zerolinecolor='black',
                         secondary_y=False, title=dict(standoff=2))
        fig.update_yaxes(range=[0, max(df_7.porcentagem_acumulada) + 10],
                         showgrid=True, gridwidth=gridwidth, secondary_y=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=False)

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-18-px', 'figure'),
               Output('chart-18-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('slider-1', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_18_px(theme, slide, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)
    df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
        df_2.despesas_faturamento == 'faturamento')]
    #df_3 = df_3[df_3['descricao'].str.startswith('Venda')]
    df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
    df_4['months_mean'] = df_4.valor_original.mean()

    if not df_4.empty:

        slide_var = "{:,.2f}".format(slide).replace(
            ',', 'v').replace('.', ',').replace('v', '.')
        mes_str = "<span style='font-size:15px;color:#686868;'>Média: " + df_4.mes_ano.values[0] + \
            " ~ " + df_4.mes_ano.values[-1] + \
            " (" + slide_var + ")<br></span>"

        fig = go.Figure(
            go.Indicator(
                mode="number+gauge+delta",
                value=df_4.valor_original.values[-1],
                #number={'suffix': "%" },
                domain={"x": [0.5, 0.5], "y": [0.5, 0.5]},
                title={'text': mes_str},
                delta={'reference': slide,
                       'relative': True, 'valueformat': '.2%'},
                gauge={
                    'bar': {'color': '#43aa8b'},
                    'shape': "angular",  # bullet
                    'axis': {'range': [1000, df_4.months_mean.values[0] * 1.5]},
                    # 'threshold': {
                    # 'line': {'color': "lightgray", 'width': 3},
                    # 'thickness': 0,
                    # 'value': slide},
                    'steps': [
                        {'range': [0, slide], 'color': "#C8C8C8"},
                        #{'range': [150, 250], 'color': "gray"}
                    ]}))

        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, t=0, b=0),
            height=None,
            width=None,
            separators=',.',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            modebar=mode_bar,
            template=theme_light if theme else theme_dark,
        )

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-19-px', 'figure'),
               Output('chart-19-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('slider-2', 'value'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value')])
def chart_19_px(theme, slide, inicial_date, final_date):
    
    df_2 = get_dataframe_2(inicial_date, final_date)
    df_3 = df_2.loc[(df_2.operacao == 'Débito') & (
        df_2.despesas_faturamento == 'despesas')]
    df_3['valor_original'] = df_3.valor_original * -1
    df_4 = df_3.groupby(['mes_num', 'ano', 'mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num'], ascending=True, inplace=True)
    df_4['months_mean'] = df_4.valor_original.mean()

    if not df_4.empty:

        slide_var = "{:,.2f}".format(slide).replace(
            ',', 'v').replace('.', ',').replace('v', '.')
        mes_str = "<span style='font-size:15px;color:#686868;'>Média: " + df_4.mes_ano.values[0] + \
            " ~ " + df_4.mes_ano.values[-1] + \
            " (" + slide_var + ")<br></span>"

        fig = go.Figure(
            go.Indicator(
                mode="number+gauge+delta",
                value=df_4.valor_original.values[-1],
                #number={'suffix': "%" },
                domain={"x": [0.5, 0.5], "y": [0.5, 0.5]},
                title={'text': mes_str},
                delta={'reference': slide,
                       'relative': True, 'valueformat': '.2%'},
                gauge={
                    'bar': {'color': '#f94144'},
                    'shape': "angular",  # bullet
                    'axis': {'range': [1000, df_4.months_mean.values[0] * 1.5]},
                    # 'threshold': {
                    # 'line': {'color': "lightgray", 'width': 3},
                    # 'thickness': 0,
                    # 'value': slide},
                    'steps': [
                        {'range': [0, slide], 'color': "#C8C8C8"},
                        #{'range': [150, 250], 'color': "gray"}
                    ]}))

        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, t=0, b=0),
            height=None,
            width=None,
            separators=',.',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            modebar=mode_bar,
            template=theme_light if theme else theme_dark,
        )

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=42, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-20-px', 'figure'),
               Output('chart-20-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value'),
               Input('radioitem-14', 'value')])
def chart_20_px(theme, inicial_date, final_date, modo):
    
    df_2 = get_dataframe_2(inicial_date, final_date)

    if modo == 'Despesas':
        df_3 = df_2.loc[(df_2.operacao == 'Débito') & (
            df_2.despesas_faturamento == 'despesas')]
        df_3['valor_original'] = df_3.valor_original * -1
    else:
        df_3 = df_2.loc[(df_2.operacao == 'Crédito') & (
            df_2.despesas_faturamento == 'faturamento')]

    df_4 = df_3.groupby(['mes_num', 'dia', 'ano', 'dia_mes_ano'], as_index=False)[
        'valor_original'].sum()
    df_4.sort_values(['ano', 'mes_num', 'dia'], ascending=True, inplace=True)

    if not df_4.empty:

        fig = px.histogram(df_4,
                           x='dia_mes_ano',
                           y='valor_original',
                           color="ano",
                           color_discrete_sequence=px.colors.qualitative.Dark2,
                           template=theme_light if theme else theme_dark)

        fig.update_layout(
            yaxis_type='log',
            separators=',.',
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            # clickmode='event+select',
            modebar=mode_bar,
            bargap=0.7 if len(df_4) == 1 else 0.1, # Largura reduzida quando for uma barra
            #yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            #xaxis={'categoryorder': 'total ascending'}
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black'),),
            template=theme_light if theme else theme_dark,
        )

        fig.update_yaxes(showgrid=True, gridwidth=gridwidth,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=True)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        fig.update_traces(
            hovertemplate=' %{y:,.2f}<extra></extra> ')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=40, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-21-px', 'figure'),
               Output('chart-21-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value'),
               Input('radioitem-15', 'value')])
def chart_21_px(theme, inicial_date, final_date, modo):
    
    df_2 = get_dataframe_main().copy()

    df_2 = df_2.loc[(df_2.data_movimento >= inicial_date)
                    & (df_2.data_movimento <= final_date)]

    if modo == 'Crédito':
        df_3 = df_2.loc[(df_2.operacao == 'Crédito') &
                        (df_2.situacao == 'Atrasado')]
    else:
        df_3 = df_2.loc[(df_2.operacao == 'Débito') &
                        (df_2.situacao == 'Atrasado')]
        df_3['valor_original'] = df_3.valor_original * -1

    df_3 = df_3[['data_movimento', 'data_original_vencimento', 'valor_original', 'situacao',
                 'ano', 'mes_num', 'dia', 'dia_mes_ano', 'fornecedor_cliente', 'categoria_nova']]

    df_3 = df_3.groupby(['categoria_nova', 'situacao']
                        ).size().reset_index(name='contagem')

    if not df_3.empty:

        fig = px.histogram(df_3,
                           x='categoria_nova',
                           y='contagem',
                           color_discrete_sequence=['#f9844a'],
                           template=theme_light if theme else theme_dark)

        fig.update_layout(
            yaxis_type='log',
            separators=',.',
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            #yaxis_title='Dias em atraso',
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            clickmode='event+select',
            modebar=mode_bar,
            bargap=0.7 if len(df_3) == 1 else 0.1, # Largura reduzida quando for uma barra
            #yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            xaxis={'categoryorder': 'total ascending'},
            hovermode="x unified",
            hoverlabel=dict(bgcolor='white', font=dict(color='black')),
        )

        fig.update_yaxes(showgrid=False, gridwidth=gridwidth, visible=False)
        fig.update_xaxes(showgrid=False, gridwidth=gridwidth, visible=False)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=12))

        fig.update_traces(hovertemplate=' Contas em atraso: %{y} ')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=40, color="#DCDCDC"), textangle=30)"""
    return [fig, {'visibility': 'visible'}]


@callback([Output('chart-22-px', 'figure'),
               Output('chart-22-px', 'style')],
              [Input(ThemeSwitch.ids.switch('theme-2'), 'checked'),
               Input('date-picker-1', 'value'),
               Input('date-picker-2', 'value'),
               Input('chart-21-px', 'selectedData'),
               Input('radioitem-15', 'value')])
def chart_22_px(theme, inicial_date, final_date, click_bar, operacao):
    
    df_2 = get_dataframe_main().copy()
    df_2 = df_2.loc[(df_2.data_movimento >= inicial_date)
                    & (df_2.data_movimento <= final_date)]
    df_2.sort_values(['data_original_vencimento'],
                     ascending=True, inplace=True)
    df_2.reset_index(drop=True)

    global operacao_var, inicial_date_var_1, final_date_var_1
    if (operacao != operacao_var) | (inicial_date != inicial_date_var_1) | (final_date != final_date_var_1):
        operacao_var = operacao
        inicial_date_var_1 = inicial_date
        final_date_var_1 = final_date
        click_bar = None

    if click_bar is not None:
        list_filter = []
        for i in range(len(click_bar['points'])):
            list_filter.append(click_bar['points'][i]['x'])

        df_2 = df_2.loc[(df_2.categoria_nova.isin(list_filter))
                        & (df_2.situacao == 'Atrasado')]
    else:
        df_2 = df_2.loc[(df_2.operacao == operacao) &
                        (df_2.situacao == 'Atrasado')]

    df_2['valor_original'] = abs(df_2.valor_original)

    df_2['dia'] = df_2['data_original_vencimento'].dt.day
    df_2['dia_mes_ano'] = df_2['data_original_vencimento'].dt.strftime(
        '%d %b-%y').str.title()
    df_2['mes_ano'] = pd.to_datetime(df_2['data_original_vencimento']).dt.strftime(
        '%b-%y').apply(lambda x: x.capitalize())
    df_2['ano'] = df_2['data_original_vencimento'].dt.year
    df_2['mes_num'] = df_2['data_original_vencimento'].dt.month

    df_3 = df_2[['data_movimento', 'data_original_vencimento', 'valor_original', 'situacao',
                 'ano', 'mes_num', 'dia', 'dia_mes_ano', 'fornecedor_cliente', 'categoria_nova']]

    df_3['dias_atrasado'] = (pd.to_datetime(
        'today').normalize() - df_3['data_original_vencimento']).dt.days

    #df_3.sort_values(['data_original_vencimento'], ascending=True, inplace=True)
    df_3.sort_index(ascending=True, inplace=True)

    if not df_3.empty:

        fig = px.scatter(df_3,
                         x='dias_atrasado',
                         y='valor_original',
                         size='dias_atrasado',
                         size_max=40,
                         opacity=0.7,
                         color='fornecedor_cliente',
                         color_discrete_sequence=px.colors.qualitative.Bold,
                         custom_data=['dia_mes_ano', 'dias_atrasado', 'fornecedor_cliente',
                                      'valor_original', 'categoria_nova'],)

        fig.update_layout(
            yaxis_type='log',
            # xaxis_type='log',
            separators=',.',
            autosize=True,
            margin=fig_margin,
            height=None,
            width=None,
            yaxis_title=None,
            xaxis_title=None,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
            legend_title=None,
            clickmode='event+select',
            modebar=mode_bar,
            bargap=0.1,
            #yaxis_tickprefix='R$ ',
            # yaxis_tickformat=',.2f',
            xaxis={'categoryorder': 'total ascending'},
            #hovermode="x unified",
            #hoverlabel=dict(bgcolor='white', font=dict(color='black')),
            template=theme_light if theme else theme_dark,
            
        )
        
        fig.update_layout(legend=dict(
            x=0, y=-0.2,
            traceorder='normal',
            font=dict(size=11),
            #bgcolor='white',
            bordercolor='grey',
            borderwidth=0.5,
            orientation="h",
            itemclick="toggleothers",
            itemdoubleclick="toggle",
            #yanchor='middle',
            #xanchor='right'
            ))


        fig.update_yaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(showgrid=True, gridwidth=gridwidth, visible=True,
                         gridcolor='#E0E0E0' if theme else '#484848',)
        fig.update_xaxes(tickangle=0, tickfont=dict(size=12))

        fig.update_traces(hovertemplate=' %{customdata[2]}<extra></extra><br> Vencimento: %{customdata[0]}'
                          ' <br> Dias em atraso: %{customdata[1]} <br> valor: %{customdata[3]:,.2f} <br>'
                          ' Categoria: %{customdata[4]}')

    else:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor=plotbg_color_light if theme else plotbg_color_dark,
                          paper_bgcolor=plotbg_color_light if theme else plotbg_color_dark)
        fig.update_yaxes(showgrid=False, visible=False)
        fig.update_xaxes(showgrid=False, visible=False)
        fig.add_annotation(text="Sem registros", xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=30, color='grey'), textangle=0)

    """fig.add_annotation(text="DEMONSTRAÇÃO", xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=40, color="#DCDCDC"), textangle=30)"""

    return [fig, {'visibility': 'visible'}]


