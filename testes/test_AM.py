import pytest
import pandas as pd
from unittest.mock import patch

# Importa funções do app principal (modifique conforme o nome do seu arquivo principal)
from pages.Analysis_Market import fetch_data, fetch_sector_data, fetch_trending_indices, fetch_crypto_data

# --------------------------
# Testes da função fetch_data
# --------------------------
@patch("pages.Analysis_Market.yf.download")
def test_fetch_data_valid(mock_download):
    # Simula retorno do yfinance
    mock_download.return_value = pd.DataFrame({
        "Close": [100, 110, 120]
    })

    df = fetch_data("^GSPC", "1y")
    assert not df.empty
    assert "^GSPC" in df.columns

@patch("pages.Analysis_Market.yf.download")
def test_fetch_data_invalid(mock_download):
    # Simula retorno vazio
    mock_download.return_value = pd.DataFrame()
    df = fetch_data("INVALID", "1y")
    assert df is None

# --------------------------
# Testes da função fetch_sector_data
# --------------------------
@patch("pages.Analysis_Market.yf.download")
def test_fetch_sector_data(mock_download):
    mock_download.return_value = pd.DataFrame({
        "Close": [10, 15]
    })
    df = fetch_sector_data(["XLK"], period="1y")
    assert not df.empty
    assert "XLK" in df.index

# --------------------------
# Testes da função fetch_trending_indices
# --------------------------
@patch("pages.Analysis_Market.yf.download")
def test_fetch_trending_indices(mock_download):
    mock_download.return_value = pd.DataFrame({
        "Close": [2000, 2100]
    })
    df = fetch_trending_indices(["^GSPC"])
    assert not df.empty
    assert "^GSPC" in df.index

# --------------------------
# Testes da função fetch_crypto_data
# --------------------------
@patch("pages.Analysis_Market.requests.get")
def test_fetch_crypto_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "image": "url",
            "current_price": 30000,
            "market_cap": 1000000000,
            "total_volume": 50000000,
            "price_change_percentage_24h": 2.5
        }
    ]

    result = fetch_crypto_data()
    assert isinstance(result, list)
    assert result[0]["id"] == "bitcoin"

