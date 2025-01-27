# Importing libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Backtest",
    page_icon=":chart_with_upwards_trend:"
)

@st.cache_data
def fetch_index_data(ticker):
    """
    Fetch historical data for a single index.
    """
    data = yf.download(ticker, period="10y", interval="1d")
    data.reset_index(inplace=True)
    return data[['Date', 'Close']]

# User inputs
st.title(":chart_with_upwards_trend: Backtest")
st.sidebar.header("Parâmetros de Backtesting")

ticker = st.sidebar.selectbox(
    "Selecione o Indíce para Backtesting:",
    options={
        '^GDAXI': 'Germany - DAX',
        '^FCHI': 'France - CAC 40',
        '^FTSE': 'UK - FTSE 100',
        '^BVSP': 'Brazil - IBOVESPA',
        '^N225': 'Japan - Nikkei 225',
    }.keys(),
    format_func=lambda x: f"{x} ({dict({ '^GDAXI': 'Germany - DAX', '^FCHI': 'France - CAC 40', '^FTSE': 'UK - FTSE 100', '^BVSP': 'Brazil - IBOVESPA', '^N225': 'Japan - Nikkei 225' })[x]})"
)

initial_investment = st.sidebar.number_input(
    "Quantia Inicial ($):",
    min_value=100.0,
    value=10000.0
)

moving_average_window = st.sidebar.slider(
    "Dias da Janela de Média Móvel :",
    min_value=10,
    max_value=200,
    value=50
)

buy_threshold = st.sidebar.slider(
    "Sinal de Compra (% abaixo da Média):",
    min_value=1.0,
    max_value=20.0,
    value=5.0
)

sell_threshold = st.sidebar.slider(
    "Sinal de Venda (% acima da Média):",
    min_value=1.0,
    max_value=20.0,
    value=5.0
)

# Fetch index data
data = fetch_index_data(ticker)

# Calculate moving average
data['MA'] = data['Close'].rolling(window=moving_average_window).mean()

# Add buy/sell signals
data['Buy Signal'] = data['Close'] < (1 - buy_threshold / 100) * data['MA']
data['Sell Signal'] = data['Close'] > (1 + sell_threshold / 100) * data['MA']

# Simulate trading strategy
cash = initial_investment
position = 0  # Number of units held
data['Portfolio Value'] = 0.0  # Track portfolio value

for i in range(len(data)):
    if data.loc[i, 'Buy Signal'] and cash > 0:
        # Buy as many units as possible
        position = cash / data.loc[i, 'Close']
        cash = 0  # Use all available cash
    elif data.loc[i, 'Sell Signal'] and position > 0:
        # Sell all units
        cash = position * data.loc[i, 'Close']
        position = 0
    # Update portfolio value
    data.loc[i, 'Portfolio Value'] = cash + (position * data.loc[i, 'Close'])

# Display results
st.header("Resultados do Backtest")
st.line_chart(data[['Date', 'Portfolio Value']].set_index('Date'))

# Final metrics
final_portfolio_value = data.iloc[-1]['Portfolio Value']
total_return = (final_portfolio_value / initial_investment - 1) * 100
st.metric("Valor Final ($)", f"{final_portfolio_value:,.2f}")
st.metric("Retorno Cumulativo (%)", f"{total_return:,.2f}%")

# Display raw data (optional)
if st.checkbox("Mostrar planilha"):
    st.write(data)
