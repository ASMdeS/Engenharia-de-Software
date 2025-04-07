import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Define the title and icon for the app
st.set_page_config(
    page_title='Backtesting para Ações',
    page_icon=':chart_with_upwards_trend:',
)

# Backtesting Logic for Moving Average Crossover
def backtest_ma_crossover(data, short_window, long_window):
    """
    Backtest a simple moving average crossover strategy.

    Args:
        data (pd.DataFrame): The historical market data.
        short_window (int): The window for the short moving average.
        long_window (int): The window for the long moving average.

    Returns:
        pd.DataFrame: The DataFrame with strategy results.
    """
    # Make a copy to avoid modifying the original data
    results = data.copy()

    # Calculate moving averages
    results['Short MA'] = results['Close'].rolling(window=short_window).mean()
    results['Long MA'] = results['Close'].rolling(window=long_window).mean()

    # Generate trading signals
    results['Signal'] = 0
    # Reset index to avoid alignment issues
    results = results.reset_index(drop=True)
    # Now apply the conditions
    results.loc[results['Short MA'] > results['Long MA'], 'Signal'] = 1
    results.loc[results['Short MA'] <= results['Long MA'], 'Signal'] = -1

    # Calculate returns
    results['Daily Return'] = results['Close'].pct_change()
    results['Strategy Return'] = results['Signal'].shift(1) * results['Daily Return']

    # Fill NaN values with 0
    results['Strategy Return'] = results['Strategy Return'].fillna(0)

    return results


# Backtesting Logic for RSI
def backtest_rsi(data, window, oversold, overbought):
    """
    Backtest a Relative Strength Index (RSI) strategy.

    Args:
        data (pd.DataFrame): The historical market data.
        window (int): The window for RSI calculation.
        oversold (int): RSI level to consider oversold.
        overbought (int): RSI level to consider overbought.

    Returns:
        pd.DataFrame: The DataFrame with strategy results.
    """
    # Make a copy to avoid modifying the original data
    results = data.copy()

    # Calculate daily price changes
    delta = results['Close'].diff()

    # Create up and down price movements
    up = delta.copy()
    up[up < 0] = 0
    down = -delta.copy()
    down[down < 0] = 0

    # Calculate the EWMA (Exponential Weighted Moving Average)
    roll_up = up.ewm(span=window).mean()
    roll_down = down.ewm(span=window).mean()

    # Calculate RS (Relative Strength)
    RS = roll_up / roll_down

    # Calculate RSI
    results['RSI'] = 100.0 - (100.0 / (1.0 + RS))

    # Generate trading signals
    results['Signal'] = 0
    # Reset index to avoid alignment issues
    results = results.reset_index(drop=True)
    # Now apply the conditions
    results.loc[results['RSI'] < oversold, 'Signal'] = 1  # Buy signal when oversold
    results.loc[results['RSI'] > overbought, 'Signal'] = -1  # Sell signal when overbought

    # Calculate returns
    results['Daily Return'] = results['Close'].pct_change()
    results['Strategy Return'] = results['Signal'].shift(1) * results['Daily Return']

    # Fill NaN values with 0
    results['Strategy Return'] = results['Strategy Return'].fillna(0)

    return results
# ----------------------------------------------------------------------------
# Helper functions

@st.cache_data
def get_ticker_data(ticker):
    """Get historical data for a specific stock ticker"""
    try:
        data = yf.download(ticker, period="10y", interval="1d")
        if data.empty:
            st.error(f"Não foi encontrado o ticker {ticker}. Revise o ticker e tente novamente.")
            return None
        data.reset_index(inplace=True)
        return data[['Date', 'Close']]
    except Exception as e:
        st.error(f"Erro ao buscar dados para o ticker {ticker}: {str(e)}")
        return None


# ----------------------------------------------------------------------------
# Application UI
st.title(':chart_with_upwards_trend: Ferramenta de Backtesting de Ações')
st.write('Simulando e analisando estratégias de trade com base em dados históricos de ações')

# Stock ticker input
ticker_input = st.text_input('Digite o Ticker:', 'AAPL')

# Fetch data for the specified ticker
stock_data = get_ticker_data(ticker_input)

if stock_data is not None:
    # Convert pandas.Timestamp to datetime.date for the slider
    min_date = stock_data['Date'].min().date()
    max_date = stock_data['Date'].max().date()

    # Date range selector
    from_date, to_date = st.slider(
        'Selecione o período de tempo para backtest:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Convert from_date and to_date to datetime64[ns]
    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)

    # Filter data based on selected date range
    filtered_data = stock_data[
        (stock_data['Date'] >= from_date) &
        (stock_data['Date'] <= to_date)
        ]

    # Strategy Parameters
    st.sidebar.header('Parâmetros da Estratégia')
    strategy_type = st.sidebar.selectbox(
        'Selecione a Estratégia:',
        ['Moving Average Crossover', 'RSI']
    )

    if strategy_type == 'Moving Average Crossover':
        short_window = st.sidebar.number_input('Janela da Média Móvel Curta:', min_value=1, value=10, step=1)
        long_window = st.sidebar.number_input('Janela da Média Móvel Longa:', min_value=1, value=30, step=1)

        # Run backtest with MA Crossover
        backtest_results = backtest_ma_crossover(filtered_data, short_window, long_window)



    elif strategy_type == 'RSI':
        window = st.sidebar.number_input('Janela do RSI:', min_value=1, value=14, step=1)
        oversold = st.sidebar.number_input('Nível de Sobrevenda:', min_value=1, max_value=100, value=30, step=1)
        overbought = st.sidebar.number_input('Nível de Sobrecompra:', min_value=1, max_value=100, value=70, step=1)

        # Run backtest with RSI
        backtest_results = backtest_rsi(filtered_data, window, oversold, overbought)

    # Calculate equity curve
    backtest_results['Equity Curve'] = (1 + backtest_results['Strategy Return']).cumprod()
    backtest_results['Buy and Hold'] = (1 + backtest_results['Daily Return']).cumprod()
    backtest_results['Buy and Hold'] = backtest_results['Buy and Hold'].fillna(1)

    # Display charts
    st.subheader(f'Resultados do Backtesting para {ticker_input}')

    # Price and signals chart
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(backtest_results['Date'], backtest_results['Close'], label='Preço de Fechamento')

    if strategy_type == 'Moving Average Crossover':
        ax1.plot(backtest_results['Date'], backtest_results['Short MA'], label=f'MM de {short_window} dias')
        ax1.plot(backtest_results['Date'], backtest_results['Long MA'], label=f'MM de {long_window} dias')

    elif strategy_type == 'RSI':
        # Create a second y-axis for RSI
        ax2 = ax1.twinx()
        ax2.plot(backtest_results['Date'], backtest_results['RSI'], 'g-', label='RSI')
        ax2.axhline(y=oversold, color='g', linestyle='--')
        ax2.axhline(y=overbought, color='r', linestyle='--')
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend(loc='upper right')

    # Plot buy/sell signals
    buy_signals = backtest_results[backtest_results['Signal'] == 1]
    sell_signals = backtest_results[backtest_results['Signal'] == -1]

    ax1.scatter(buy_signals['Date'], buy_signals['Close'], marker='^', color='g', s=100, label='Compra')
    ax1.scatter(sell_signals['Date'], sell_signals['Close'], marker='v', color='r', s=100, label='Venda')

    ax1.set_title(f'{ticker_input} - Preço e Sinais')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Preço')
    ax1.legend(loc='upper left')
    st.pyplot(fig1)

    # Equity curve chart
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(backtest_results['Date'], backtest_results['Equity Curve'], label='Estratégia')
    ax2.plot(backtest_results['Date'], backtest_results['Buy and Hold'], label='Comprar e Segurar')
    ax2.set_title(f'{ticker_input} - Curva de Patrimônio')
    ax2.set_xlabel('Data')
    ax2.set_ylabel('Patrimônio')
    ax2.legend()
    st.pyplot(fig2)

    # Show summary metrics
    st.subheader('Métricas de Desempenho')

    # Calculate metrics
    total_days = len(backtest_results)
    strategy_return = backtest_results['Equity Curve'].iloc[-1] - 1
    buy_hold_return = backtest_results['Buy and Hold'].iloc[-1] - 1

    # Annualized returns (assuming 252 trading days per year)
    years = total_days / 252
    annualized_strategy_return = (1 + strategy_return) ** (1 / years) - 1 if years > 0 else 0
    annualized_buy_hold_return = (1 + buy_hold_return) ** (1 / years) - 1 if years > 0 else 0

    # Maximum drawdown
    strategy_cummax = backtest_results['Equity Curve'].cummax()
    strategy_drawdown = (backtest_results['Equity Curve'] / strategy_cummax) - 1
    max_drawdown = strategy_drawdown.min()

    # Sharpe ratio (assuming risk-free rate of 0)
    strategy_daily_returns = backtest_results['Strategy Return']
    sharpe_ratio = np.sqrt(
        252) * strategy_daily_returns.mean() / strategy_daily_returns.std() if strategy_daily_returns.std() > 0 else 0

    # Number of trades
    signal_changes = backtest_results['Signal'].diff().fillna(0)
    num_trades = (signal_changes != 0).sum()

    # Create metrics columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Retorno Total (Estratégia)", f"{strategy_return:.2%}")
        st.metric("Retorno Anualizado (Estratégia)", f"{annualized_strategy_return:.2%}")
        st.metric("Drawdown Máximo", f"{max_drawdown:.2%}")
        st.metric("Número de Operações", num_trades)

    with col2:
        st.metric("Retorno Total (Comprar e Segurar)", f"{buy_hold_return:.2%}")
        st.metric("Retorno Anualizado (Comprar e Segurar)", f"{annualized_buy_hold_return:.2%}")
        st.metric("Índice Sharpe", f"{sharpe_ratio:.2f}")
        st.metric("Desempenho Superior", f"{strategy_return - buy_hold_return:.2%}")

    # Display the last few trades
    st.subheader('Operações Recentes')

    # Get all signal changes
    trades = backtest_results[signal_changes != 0].copy()
    trades['Action'] = trades['Signal'].apply(lambda x: 'Compra' if x == 1 else 'Venda' if x == -1 else 'Desconhecido')

    if not trades.empty:
        trades_display = trades[['Date', 'Action', 'Close']].tail(10)
        trades_display['Date'] = trades_display['Date'].dt.date
        trades_display.columns = ['Data', 'Ação', 'Preço']
        st.table(trades_display)
    else:
        st.write("Nenhuma operação foi gerada no período selecionado.")
else:
    st.write("Por favor, insira um símbolo de ticker de ação válido.")
    