from behave import given, when, then
import pandas as pd
from pages.Analysis_Market import fetch_data, fetch_sector_data, fetch_trending_indices, fetch_crypto_data

@given('que eu tenho o ticker "{ticker}" e o período "{periodo}"')
def passo_dado_ticker_periodo(context, ticker, periodo):
    context.ticker = ticker
    context.periodo = periodo

@when("eu busco os dados do ativo")
def passo_quando_buscar_dados(context):
    context.df = fetch_data(context.ticker, context.periodo)

@then('o resultado deve ser um DataFrame não vazio com "{ticker}" nas colunas')
def passo_entao_validar_dataframe(context, ticker):
    assert isinstance(context.df, pd.DataFrame)
    assert not context.df.empty
    assert ticker in context.df.columns

@given('que eu tenho uma lista de setores {setores} e o período "{periodo}"')
def passo_dado_lista_setores(context, setores, periodo):
    context.setores = eval(setores)
    context.periodo = periodo

@when("eu busco os dados dos setores")
def passo_quando_buscar_setores(context):
    context.resultado = fetch_sector_data(context.setores, context.periodo)

@then("o resultado deve ser uma série não vazia ordenada de forma decrescente")
def passo_entao_validar_serie_setores(context):
    assert isinstance(context.resultado, pd.Series)
    assert not context.resultado.empty
    assert context.resultado.is_monotonic_decreasing

@given('que eu tenho uma lista de índices {indices} e o período "{periodo}"')
def passo_dado_lista_indices(context, indices, periodo):
    context.indices = eval(indices)
    context.periodo = periodo

@when("eu busco os dados dos índices")
def passo_quando_buscar_indices(context):
    context.series = fetch_trending_indices(context.indices, context.periodo)

@then("o resultado deve ser uma série de floats não vazia")
def passo_entao_validar_serie_indices(context):
    assert isinstance(context.series, pd.Series)
    assert not context.series.empty
    assert all(isinstance(val, float) for val in context.series.values)

@when("eu busco os dados das criptomoedas")
def passo_quando_buscar_cripto(context):
    context.cripto = fetch_crypto_data()

@then("o resultado deve ser uma lista não vazia com informações válidas")
def passo_entao_validar_dados_cripto(context):
    assert isinstance(context.cripto, list)
    assert len(context.cripto) > 0
    assert "id" in context.cripto[0]
