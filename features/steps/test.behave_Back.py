import pandas as pd
from behave import given, when, then
from testes.helpers.mock_data import gerar_dados_mock
from pages.Backtesting import backtest_ma_crossover, backtest_rsi

@given("que eu tenho dados históricos simulados")
def step_impl(context):
    context.dados = gerar_dados_mock()

@when('eu aplico a estratégia de média móvel com janelas 5 e 20')
def step_impl(context):
    context.resultado = backtest_ma_crossover(context.dados, 5, 20)

@when('eu aplico a estratégia RSI com janela 14, sobrevenda 30 e sobrecompra 70')
def step_impl(context):
    context.resultado = backtest_rsi(context.dados, 14, 30, 70)

@then('o resultado deve conter colunas "Short MA", "Long MA" e "Strategy Return"')
def step_impl(context):
    for coluna in ["Short MA", "Long MA", "Strategy Return"]:
        assert coluna in context.resultado.columns, f"Coluna {coluna} não encontrada"

@then('o resultado deve conter colunas "RSI" e "Strategy Return"')
def step_impl(context):
    for coluna in ["RSI", "Strategy Return"]:
        assert coluna in context.resultado.columns, f"Coluna {coluna} não encontrada"
