import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from bs4 import BeautifulSoup

# Configuração da página
st.set_page_config(page_title="Análise de Mercado", page_icon=":chart_with_upwards_trend:", layout="centered")

# Título Principal
st.title(":chart_with_upwards_trend: Análise de Mercado")



# Criando abas
tab1, tab2, tab3= st.tabs(["📈 Comparação de Índices", "🏦 Análise de Setores", "🪙 Análise Crypto"])

with tab1:
    st.markdown("🔍 Digite o código de um índice e pressione **Enter** para adicioná-lo ao gráfico. Exemplos: **^GSPC** (S&P 500), **^BVSP** (IBOVESPA), **^IXIC** (NASDAQ).")

    # Inicializa variáveis no session_state
    if "selected_indices" not in st.session_state:
        st.session_state.selected_indices = set()

    if "ticker_input" not in st.session_state:
        st.session_state.ticker_input = ""

    if "update_trigger" not in st.session_state:
        st.session_state.update_trigger = False

    # Input do ticker
    st.subheader("📌 Digite o Ticker do Índice e pressione Enter:")
    st.text_input(
        "Digite o código do índice:",
        key="ticker_input",
        on_change=lambda: add_ticker(st.session_state.ticker_input)
    )

    # Escolher o período de análise
    st.subheader("⏳ Escolha o Período de Análise:")
    periodo = st.selectbox("Selecione um período:", ["1y", "5y", "10y", "max"])

    @st.cache_data
    def fetch_data(ticker, period="1y"):
        """Busca dados históricos de um índice."""
        try:
            df = yf.download(ticker, period=period, interval="1d")
            if "Close" in df.columns:
                df = df[["Close"]].dropna()
                df.rename(columns={"Close": ticker}, inplace=True)
                return df
        except Exception:
            return None
        return None

    # 🔹 Função para adicionar índice
    def add_ticker(ticker):
        ticker = ticker.strip().upper()
        if ticker in st.session_state.selected_indices:
            st.warning(f"⚠️ O índice {ticker} já foi adicionado.")
            return

        if ticker:
            df = fetch_data(ticker, period=periodo)
            if df is not None and not df.empty:
                st.session_state.selected_indices.add(ticker)
                st.session_state.ticker_input = ""
                st.session_state.update_trigger = not st.session_state.update_trigger
            else:
                st.error("❌ Nenhum dado válido foi encontrado para o ticker digitado.")

    # 🔹 Exibir índices adicionados
    selected_indices_list = list(st.session_state.selected_indices)

    if selected_indices_list:
        st.subheader("📌 Índices Selecionados:")
        indices_para_manter = set(selected_indices_list)

        for ticker in selected_indices_list:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📈 {ticker}")
            with col2:
                if st.button(f"❌ Remover {ticker}", key=f"remove_{ticker}"):
                    indices_para_manter.remove(ticker)
                    st.session_state.selected_indices = indices_para_manter
                    st.session_state.update_trigger = not st.session_state.update_trigger
                    st.rerun()

        # 🔹 Gerar gráfico de evolução dos índices
        data_frames = [fetch_data(ticker, period=periodo) for ticker in st.session_state.selected_indices if fetch_data(ticker, period=periodo) is not None]

        if data_frames:
            df_final = pd.concat(data_frames, axis=1).dropna()
            df_final.columns = df_final.columns.get_level_values(0)
            st.subheader("📊 Evolução dos Índices:")
            st.line_chart(df_final)
        else:
            st.warning("⚠️ Nenhum dado válido para os índices selecionados.")
    else:
        st.warning("🔍 Nenhum índice selecionado. Digite um ticker para começar.")

# Aba de Análise de Setores
with tab2:   
    st.subheader("🏦 Análise de Setores")

    setores_dict = {
        "XLK": "Tecnologia 💻", "XLE": "Energia ⚡", "XLF": "Financeiro 🏦",
        "XLV": "Saúde 🏥", "XLY": "Consumo Discricionário 🛒", "XLP": "Consumo Básico 🏠",
        "XLU": "Utilidades Públicas 💡", "XLI": "Indústria 🏭"
    }

    periodo_setores = st.selectbox("Escolha o Período de Análise:", ["1mo", "6mo", "1y", "5y", "max"])

    @st.cache_data
    def fetch_sector_data(tickers_list, period="1y"):
        """Busca a variação percentual dos setores"""
        data = {}

        for ticker in tickers_list:
            try:
                df = yf.download(ticker, period=period, interval="1d")
                if "Close" in df.columns and not df.empty:
                    df = df["Close"].dropna()

                    if len(df) > 1:
                        var_pct = ((df.iloc[-1] / df.iloc[0]) - 1) * 100
                        data[ticker] = var_pct
            except Exception:
                pass

        if data:
            trend_series = pd.Series(data).dropna()
            trend_series = trend_series.astype(float)
            return trend_series.sort_values(ascending=False)

        return pd.Series(dtype=float)

    df_setores = fetch_sector_data(list(setores_dict.keys()), period=periodo_setores)

    if not df_setores.empty:
        st.subheader("📊 Desempenho dos Setores")
        setores_df = pd.DataFrame({"Setor": [setores_dict[t] for t in df_setores.index], "Variação (%)": df_setores.values})
        st.table(setores_df)

        # Criar Heatmap com Plotly Express (Treemap)
        st.subheader("📊 Heatmap de Performance dos Setores")

        # Criando um DataFrame para o treemap
        heatmap_data = pd.DataFrame(df_setores).reset_index()
        heatmap_data.columns = ["Ticker", "Variação (%)"]
        heatmap_data["Setor"] = heatmap_data["Ticker"].map(setores_dict)  
        heatmap_data["Abs Change"] = heatmap_data["Variação (%)"].abs()  # Para evitar valores nulos na dimensão

        # Criando labels com nome do setor e variação percentual abaixo
        heatmap_data["Label"] = heatmap_data.apply(lambda row: f"{row['Setor']}<br>{row['Variação (%)']:.2f}%", axis=1)

        # Definição correta da escala de cores baseada no print enviado
        color_scale = [
            [0.0, "#8B0000"],  # Vermelho escuro (≤ -3)
            [0.2, "#B22222"],  # Vermelho forte (-2)
            [0.4, "#CD5C5C"],  # Vermelho intermediário (-1)
            [0.5, "#333333"],  # Cinza escuro (0)
            [0.6, "#006400"],  # Verde escuro (1)
            [0.8, "#008000"],  # Verde intermediário (2)
            [1.0, "#00C957"]   # Verde claro (≥ 3)
        ]

        fig = px.treemap(
            heatmap_data, 
            path=["Label"],  # Agora a label inclui nome + variação percentual
            values="Abs Change",  
            color="Variação (%)",
            color_continuous_scale=color_scale,  # Escala corrigida para Plotly
            range_color=[-3, 3],  # Ajustando os valores da escala
            title="Heatmap de Setores",
            hover_data={"Variação (%)": True},
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                title="Variação (%)",
                tickvals=[-3, -2, -1, 0, 1, 2, 3],  # Mantém os valores para referência
                ticktext=["<= -3", "-2", "-1", "0", "1", "2", ">= 3"]  # Substitui -3 e 3 por <=-3 e >=3
            ),
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ Nenhum dado disponível para os setores no período selecionado.")

# Sidebar - Tendências de Investimento 🌎
st.sidebar.header("Tendências de Investimento 🌎")

indices_trend = {
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "^BVSP": "IBOVESPA",
    "^DJI": "Dow Jones",
    "^FTSE": "FTSE 100",
    "^N225": "Nikkei 225",
    "^GDAXI": "DAX Alemanha"
}

@st.cache_data
def fetch_trending_indices(_tickers_list, period="1mo"):
    """Busca a variação percentual dos índices no último mês"""
    data = {}

    for ticker in _tickers_list:
        try:
            df = yf.download(ticker, period=period, interval="1d")
            if "Close" in df.columns and not df.empty:
                df = df["Close"].dropna()

                if len(df) > 1:
                    var_pct = ((df.iloc[-1] / df.iloc[0]) - 1) * 100
                    data[ticker] = float(var_pct)  # 🔥 Garante que os valores sejam floats
        except Exception:
            pass

    if data:
        trend_series = pd.Series(data).dropna()
        trend_series = trend_series.astype(float)  # 🚀 Garante que a série seja float

        if not trend_series.empty:
            return trend_series.sort_values(ascending=False)

    return pd.Series(dtype=float)  # Retorna uma série vazia se não houver dados


trend_data = fetch_trending_indices(list(indices_trend.keys()))

if not trend_data.empty:
    st.sidebar.subheader("📈 Índices em Alta (Último Mês)")
    for ticker, valor in trend_data.items():
        st.sidebar.write(f"{indices_trend.get(ticker, ticker)}: **{valor:.2f}%**")
else:
    st.sidebar.warning("⚠️ Não conseguimos recuperar dados de tendências.")

with tab3:
    crypto_ids = [
        'bitcoin', 'ethereum', 'binancecoin', 'solana',
        'ripple', 'cardano', 'dogecoin', 'polkadot',
        'polygon', 'litecoin'
    ]

    # 🔤 Mapeamento para tickers no padrão Yahoo Finance
    crypto_symbols = {
        "bitcoin": "BTC-USD",
        "ethereum": "ETH-USD",
        "binancecoin": "BNB-USD",
        "solana": "SOL-USD",
        "ripple": "XRP-USD",
        "cardano": "ADA-USD",
        "dogecoin": "DOGE-USD",
        "polkadot": "DOT-USD",
        "polygon": "MATIC-USD",
        "litecoin": "LTC-USD"
    }

    @st.cache_data
    def fetch_crypto_data():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ','.join(crypto_ids),
            "order": "market_cap_desc",
            "per_page": len(crypto_ids),
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    data = fetch_crypto_data()

    if data:
        df = pd.DataFrame(data)
        df = df[[
            "id", "name", "symbol", "image", "current_price",
            "market_cap", "total_volume", "price_change_percentage_24h"
        ]]
        df.rename(columns={
            "id": "ID",
            "name": "Criptomoeda",
            "symbol": "Ticker",
            "image": "Logo",
            "current_price": "Preço (USD)",
            "market_cap": "Market Cap (USD)",
            "total_volume": "Volume 24h (USD)",
            "price_change_percentage_24h": "Variação 24h (%)"
        }, inplace=True)

        # 🧼 Exibe logo + nome + (ticker formatado com -USD)
        df["Criptomoeda"] = df.apply(
            lambda row: f'<img src="{row["Logo"]}" width="20" style="margin-right:5px;"> <b>{row["Criptomoeda"]}</b><br>({crypto_symbols.get(row["ID"], row["Ticker"].upper() + "-USD")})',
            axis=1
        )

        df.drop(columns=["Logo", "Ticker", "ID"], inplace=True)

        # 🔢 Formata valores
        df_styled = df.copy()
        df_styled["Preço (USD)"] = df_styled["Preço (USD)"].map('${:,.2f}'.format)
        df_styled["Market Cap (USD)"] = df_styled["Market Cap (USD)"].map('${:,.0f}'.format)
        df_styled["Volume 24h (USD)"] = df_styled["Volume 24h (USD)"].map('${:,.0f}'.format)
        df_styled["Variação 24h (%)"] = df["Variação 24h (%)"].map('{:.2f}%'.format)

        # 🎨 Cores condicionais
        def highlight_variation(val):
            try:
                val_float = float(val.replace('%', ''))
                color = 'red' if val_float < 0 else 'green'
                return f'color: {color};'
            except:
                return ''

        st.markdown("### 📈 Tabela de Cotações")
        st.write(
            df_styled.style
            .applymap(highlight_variation, subset=["Variação 24h (%)"])
            .hide(axis="index")
            .to_html(escape=False),
            unsafe_allow_html=True
        )

    else:
        st.warning("⚠️ Não foi possível carregar os dados das criptomoedas.")

# Notícias sobre o mercado financeiro
st.sidebar.header("📰 Últimas Notícias do Mercado")

def fetch_yahoo_news():
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:3]  
        return [{"title": item.title.text, "link": item.link.text} for item in items]
    return None

news = fetch_yahoo_news()

if news:
    for article in news:
        st.sidebar.markdown(f"[{article['title']}]({article['link']})")
else:
    st.sidebar.warning("⚠️ Não conseguimos encontrar notícias no momento.")

