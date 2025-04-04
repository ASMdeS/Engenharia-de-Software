import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pages.Backtesting import backtest_ma_crossover, backtest_rsi 

# Função auxiliar para criar dados fictícios
def generate_test_data(days=100):
    base_date = datetime.today()
    dates = [base_date - timedelta(days=i) for i in range(days)][::-1]
    close_prices = np.linspace(100, 200, days) + np.random.normal(0, 5, days)
    return pd.DataFrame({'Date': dates, 'Close': close_prices})


# --------------------------
# Testes para MA Crossover
# --------------------------
def test_ma_crossover_basic_behavior():
    df = generate_test_data()
    result = backtest_ma_crossover(df, short_window=5, long_window=10)
    
    assert 'Short MA' in result.columns
    assert 'Long MA' in result.columns
    assert 'Signal' in result.columns
    assert 'Strategy Return' in result.columns
    assert len(result) == len(df)
    assert result['Signal'].isin([-1, 0, 1]).all()


def test_ma_crossover_strategy_return_not_nan():
    df = generate_test_data()
    result = backtest_ma_crossover(df, short_window=5, long_window=10)
    assert result['Strategy Return'].isnull().sum() == 0


# --------------------------
# Testes para RSI
# --------------------------
def test_rsi_basic_behavior():
    df = generate_test_data()
    result = backtest_rsi(df, window=14, oversold=30, overbought=70)

    assert 'RSI' in result.columns
    assert 'Signal' in result.columns
    assert 'Strategy Return' in result.columns
    assert result['RSI'].dropna().between(0, 100).all()


def test_rsi_strategy_return_not_nan():
    df = generate_test_data()
    result = backtest_rsi(df, window=14, oversold=30, overbought=70)
    assert result['Strategy Return'].isnull().sum() == 0
