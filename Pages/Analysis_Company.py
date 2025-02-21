# Importando as bibliotecas necessárias
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt

# Definindo o título e o ícone do aplicativo
st.set_page_config(
    page_title='Análise de Ticker Financeiro',
    page_icon=':chart_with_upwards_trend:',
)

# Função para obter dados históricos de um ticker
@st.cache_data
def get_ticker_data(ticker):
    ticker_obj = yf.Ticker(ticker)  # Criando o objeto Ticker
    stock_data = ticker_obj.history(period="max", interval="1d")  # Obtendo dados históricos
    return stock_data[['Close']]  # Retorna apenas a coluna de fechamento

# Exibindo o título da página
'''
# :chart_with_upwards_trend: Análise de Ticker Financeiro

Explore o desempenho do ticker no mercado financeiro.
'''

    
# Definindo o ticker para análise
def is_valid_ticker(ticker):
    """Verifica se o ticker existe no Yahoo Finance."""
    if not ticker or ticker is None or ticker == {}:
        return False
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return 'longName' in info  # Se tiver nome da empresa, é válido
    except Exception:
        return False

# Entrada do usuário
ticker = st.text_input('Digite o Ticker:', 'AAPL')

# Validação do ticker
if ticker:
    if is_valid_ticker(ticker):
        ticker = ticker
    else:
        st.error(f"O ticker '{ticker}' não é válido. Tente outro.")
else:
    st.warning("Por favor, digite um ticker antes de continuar.")

# Rodando a função para pegar os dados do ticker
tickerChosen = yf.Ticker(ticker)
ticker_data = get_ticker_data(ticker)

# Adicionando espaço
''

# Colunas de informações estáticas sobre a ação
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.write(f"Empresa: {tickerChosen.info['longName']}")
with col2:
    st.write(f"Mercado: {tickerChosen.info['industry']}")
with col3:
    st.write(f"Preço atual: {tickerChosen.info['currentPrice']}USD")

# Informações sobre a empresa
summary =  tickerChosen.info['longBusinessSummary']
st.markdown(
    f"""
    <div style="overflow-y: scroll; height: 200px; background-color: rgba(50, 50, 50, 0.9); border-radius: 5px; padding: 10px;">
        <pre>{summary}</pre>
    </div>
    """,
    unsafe_allow_html=True
)
''
''



# Exibindo métricas do ticker
st.header(f'Métricas do Ticker {ticker}', divider='gray')

tabs = st.tabs(["Evolução de preços", "Dividendos e Descobramentos", "Informações Gerais"])

# Tab 1
with tabs[0]:
    # Convertendo pandas Timestamps para objetos datetime do Python
    min_date = ticker_data.index.min().to_pydatetime()
    max_date = ticker_data.index.max().to_pydatetime()
    # Permitindo que o usuário selecione um intervalo de tempo
    st.subheader('Gráfico de evolução')
    from_date, to_date = st.slider(
    'Evolução da ação ao longo dos anos',
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
    # Evolução de preços
    st.line_chart(
        filtered_ticker_data,
    )
    # Outra visualização
    st.subheader('Analise de evolução escolhendo o incio')
    startDat = st.text_input('Data de inicio', '2025-01-01')
    endDat = dt.date.today()
    newTime = tickerChosen.history(start = startDat, end = endDat)
    st.dataframe(newTime)
    st.download_button('Download CSV', newTime.to_csv(), file_name='evolução.csv')


# Tab 2
with tabs[1]:
    # Dividendos Pagos anualmente
    col1, col2= st.columns([1,1])
    with col1:
        st.write(f"Dividend Yield: {tickerChosen.info['dividendYield']}")
    with col2:
        st.write(f"Dividend Rate: {tickerChosen.info['dividendRate']}")
    st.subheader('Dividendos Pagos anualmente')
    dividendsYearly = tickerChosen.dividends.resample('Y').sum()
    st.bar_chart(dividendsYearly)
    st.subheader('Desddobramento das ações')
    st.dataframe(tickerChosen.splits)

# Tab 3
with tabs[2]:
    # Exbir informações contábeis
    st.subheader('Informações Contábeis')
    st.dataframe(tickerChosen.financials )
    st.download_button('Download CSV Contábil', tickerChosen.financials.to_csv(), file_name='financeiro.csv')
    st.subheader('Informações de Caixa')
    st.dataframe(tickerChosen.cashflow)
    st.download_button('Download CSV Caixa', tickerChosen.cash_flow.to_csv(), file_name='caixa.csv')

    # print(tickerChosen.info) - visualizar as infos