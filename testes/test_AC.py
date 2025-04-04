import pytest
import pandas as pd
import numpy as np
from pages.Analysis_Company import is_valid_ticker, get_ticker_data, calculate_rsi, calculate_macd
from unittest.mock import patch, MagicMock

# Teste para a função de cálculo do RSI
def test_calculate_rsi():
    prices = pd.Series([100 + i for i in range(20)])
    rsi = calculate_rsi(prices)
    assert isinstance(rsi, pd.Series)
    assert rsi.isnull().sum() > 0  # Primeiros valores devem ser NaN
    assert rsi.max() <= 100
    assert rsi.min() >= 0

# Teste para a função de cálculo do MACD
def test_calculate_macd():
    prices = pd.Series(np.linspace(100, 200, 100))
    macd, signal = calculate_macd(prices)
    assert isinstance(macd, pd.Series)
    assert isinstance(signal, pd.Series)
    assert len(macd) == len(prices)
    assert len(signal) == len(prices)


# Teste para verificar se o ticker é válido (com mock)
@patch('pages.Analysis_Company.yf.Ticker')
def test_is_valid_ticker_valid(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.info = {'longName': 'Apple Inc.'}
    mock_ticker.return_value = mock_instance
    assert is_valid_ticker('AAPL') is True

@patch('pages.Analysis_Company.yf.Ticker')
def test_is_valid_ticker_invalid(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.info = {}
    mock_ticker.return_value = mock_instance
    assert is_valid_ticker('INVALID123') is False

# Teste da função de busca de dados do ticker com cache
@patch('pages.Analysis_Company.yf.Ticker')
def test_get_ticker_data(mock_ticker):
    df_mock = pd.DataFrame({'Close': [100, 102, 105]}, index=pd.date_range("2024-01-01", periods=3))
    mock_instance = MagicMock()
    mock_instance.history.return_value = df_mock
    mock_ticker.return_value = mock_instance

    data = get_ticker_data('AAPL')
    assert isinstance(data, pd.DataFrame)
    assert 'Close' in data.columns
