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

# Add fee parameters to sidebar
commission_fee = st.sidebar.number_input(
    "Taxa de Comissão (%):",
    min_value=0.0,
    max_value=5.0,
    value=0.1,
    step=0.01,
    help="Taxa cobrada sobre o valor da transação"
)

slippage = st.sidebar.number_input(
    "Slippage (%):",
    min_value=0.0,
    max_value=5.0,
    value=0.1,
    step=0.01,
    help="Diferença estimada entre preço esperado e executado"
)

ticker = st.sidebar.selectbox(
    "Selecione o Indíce para Backtesting:",
    options={
        '^GDAXI': 'Germany - DAX',
        '^FCHI': 'France - CAC 40',
        '^FTSE': 'UK - FTSE 100',
        '^BVSP': 'Brazil - IBOVESPA',
        '^N225': 'Japan - Nikkei 225',
        '^SPX': 'USA - S&P 500',
        '^DJI': 'USA - Dow Jones Industrial Average',
        '^IXIC': 'USA - NASDAQ Composite',
        '^HSI': 'Hong Kong - Hang Seng',
        '^SSEC': 'China - Shanghai Composite',
        '^AORD': 'Australia - ASX All Ordinaries',
        '^NSEI': 'India - NSE Nifty 50',
        '^RTSI': 'Russia - RTS Index',
        '^MERV': 'Argentina - MERVAL',
        '^TA35': 'Israel - TA-35'
    }.keys(),
    format_func=lambda
        x: f"{x} ({dict({'^GDAXI': 'Germany - DAX', '^FCHI': 'France - CAC 40', '^FTSE': 'UK - FTSE 100', '^BVSP': 'Brazil - IBOVESPA', '^N225': 'Japan - Nikkei 225', '^SPX': 'USA - S&P 500', '^DJI': 'USA - Dow Jones Industrial Average', '^IXIC': 'USA - NASDAQ Composite', '^HSI': 'Hong Kong - Hang Seng', '^SSEC': 'China - Shanghai Composite', '^AORD': 'Australia - ASX All Ordinaries', '^NSEI': 'India - NSE Nifty 50', '^RTSI': 'Russia - RTS Index', '^MERV': 'Argentina - MERVAL', '^TA35': 'Israel - TA-35'})[x]})"
)

initial_investment = st.sidebar.number_input(
    "Quantia Inicial ($):",
    min_value=100.0,
    value=10000.0
)

moving_average_window = st.sidebar.slider(
    "Dias da Janela de Média Móvel:",
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

# Initialize tracking variables
cash = initial_investment
position = 0  # Number of units held
data['Portfolio Value'] = 0.0  # Track portfolio value
data['Trades'] = 0  # Track number of trades
data['Fees Paid'] = 0.0  # Track cumulative fees paid


# Function to calculate total transaction cost
def calculate_transaction_cost(price, units, commission_pct, slippage_pct):
    """Calculate total transaction cost including commission and slippage."""
    transaction_value = price * units
    commission_cost = transaction_value * (commission_pct / 100)
    slippage_cost = transaction_value * (slippage_pct / 100)
    return commission_cost + slippage_cost


# Simulate trading strategy with fees
total_fees = 0
num_trades = 0

for i in range(len(data)):
    current_price = data.loc[i, 'Close']

    if data.loc[i, 'Buy Signal'] and cash > 0:
        # Calculate maximum units we can buy after accounting for fees
        max_units = cash / (current_price * (1 + (commission_fee + slippage) / 100))
        if max_units > 0:
            # Execute buy trade
            fees = calculate_transaction_cost(current_price, max_units, commission_fee, slippage)
            position = max_units
            cash = 0  # All remaining cash used
            total_fees += fees
            num_trades += 1

    elif data.loc[i, 'Sell Signal'] and position > 0:
        # Execute sell trade
        fees = calculate_transaction_cost(current_price, position, commission_fee, slippage)
        cash = (position * current_price) - fees
        position = 0
        total_fees += fees
        num_trades += 1

    # Update portfolio value and tracking metrics
    data.loc[i, 'Portfolio Value'] = cash + (position * current_price)
    data.loc[i, 'Trades'] = num_trades
    data.loc[i, 'Fees Paid'] = total_fees

# Display results
st.header("Resultados do Backtest")
st.line_chart(data[['Date', 'Portfolio Value']].set_index('Date'))

# Final metrics
final_portfolio_value = data.iloc[-1]['Portfolio Value']
total_return = (final_portfolio_value / initial_investment - 1) * 100
total_fees_pct = (total_fees / initial_investment) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Valor Final ($)", f"{final_portfolio_value:,.2f}")
with col2:
    st.metric("Retorno Cumulativo (%)", f"{total_return:,.2f}%")
with col3:
    st.metric("Total de Trades", num_trades)

col4, col5 = st.columns(2)
with col4:
    st.metric("Total em Taxas ($)", f"{total_fees:,.2f}")
with col5:
    st.metric("Taxas sobre Capital Inicial (%)", f"{total_fees_pct:,.2f}%")

# Display raw data (optional)
if st.checkbox("Mostrar planilha"):
    st.write(data)