# Importando as bibliotecas necessárias
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Definindo o título e o ícone do aplicativo
st.set_page_config(
    page_title='Análise de Ticker Financeiro',
    page_icon=':chart_with_upwards_trend:',
)

# Função para obter dados históricos de um ticker
@st.cache_data
def get_ticker_data(ticker):
    """
    Baixa dados históricos de um ticker usando o objeto Ticker do yfinance.

    Args:
        ticker (str): O símbolo do ticker para obter dados.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados históricos do ticker.
    """
    ticker_obj = yf.Ticker(ticker)  # Criando o objeto Ticker
    stock_data = ticker_obj.history(period="10y", interval="1d")  # Obtendo dados históricos
    return stock_data[['Close']]  # Retorna apenas a coluna de fechamento

# Exibindo o título da página
'''
# :chart_with_upwards_trend: Análise de Ticker Financeiro

Explore o desempenho do ticker no mercado financeiro.
'''
# Definindo o ticker para análise
ticker = st.text_input('Digite o Ticker:', 'AAPL')  # Ticker default é AAPL (Apple)

# Rodando a função para pegar o histórico do ticker
ticker_data = get_ticker_data(ticker)

# Adicionando espaço
''
''

# Convertendo pandas Timestamps para objetos datetime do Python
min_date = ticker_data.index.min().to_pydatetime()
max_date = ticker_data.index.max().to_pydatetime()

# Permitindo que o usuário selecione um intervalo de tempo
from_date, to_date = st.slider(
    'Em que período de tempo você está interessado?',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
    format="YYYY-MM-DD"
)

# Filtrando os dados de acordo com a seleção de datas
filtered_ticker_data = ticker_data[
    (ticker_data.index <= to_date)
    & (from_date <= ticker_data.index)
]

# Plotando os dados
st.line_chart(
    filtered_ticker_data,
)

# Exibindo métricas do ticker
st.header(f'Métricas do Ticker {ticker}', divider='gray')

today = datetime.date.today()
target_date = st.date_input('Digite a data:', today)  # Ticker default é AAPL (Apple)

# Função para encontrar a data mais próxima de uma data alvo
def get_closest_date(data, target_date):
    available_dates = data.index
    closest_date = available_dates.loc[(available_dates - target_date).abs().idxmin()]
    return closest_date

# Encontrando os valores no intervalo selecionado
closest_start_date = get_closest_date(filtered_ticker_data, from_date)
closest_end_date = get_closest_date(filtered_ticker_data, to_date)

# Pegando os valores de fechamento no intervalo
start_value = filtered_ticker_data.loc[closest_start_date]['Close']
end_value = filtered_ticker_data.loc[closest_end_date]['Close']

# Calculando o crescimento
if pd.isna(start_value) or pd.isna(end_value):
    growth = 'n/a'
    delta_color = 'off'
else:
    growth = f'{end_value / start_value:,.2f}x'
    delta_color = 'normal'

# Exibindo a métrica
st.metric(
    label=f'{ticker} Index',
    value=f'{end_value:,.0f}',
    delta=growth,
    delta_color=delta_color
)