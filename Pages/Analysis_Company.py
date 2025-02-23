# Importando as bibliotecas necessárias
import streamlit as st
import yfinance as yf
import datetime as dt

# Definindo o título e o ícone do aplicativo
st.set_page_config(
    page_title='Análise de Ticker Financeiro',
    page_icon=':chart_with_upwards_trend:',
)


#Iniciando a variável
tickerChosen = None

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

# Cálculo do RSI
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Cálculo do MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

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
        # Rodando a função para pegar os dados do ticker
        tickerChosen = yf.Ticker(ticker)
        ticker_data = get_ticker_data(ticker)
    else:
        st.error(f"O ticker '{ticker}' não é válido. Tente outro.")
else:
    st.warning("Por favor, digite um ticker antes de continuar.")

# Adicionando espaço
''

# Colunas de informações estáticas sobre a ação
if tickerChosen:
    # Colunas de informações estáticas sobre a ação
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if tickerChosen.info and 'longName' in tickerChosen.info:
            st.write(f"Empresa: {tickerChosen.info['longName']}")
        else:
            st.write("Empresa: Informação indisponível")

    with col2:
        if tickerChosen.info and 'industry' in tickerChosen.info:
            st.write(f"Mercado: {tickerChosen.info['industry']}")
        else:
            st.write("Mercado: Informação indisponível")

    with col3:
        if tickerChosen.info and 'currentPrice' in tickerChosen.info:
            st.write(f"Preço atual: {tickerChosen.info['currentPrice']} USD")
        else:
            st.write("Preço atual: Informação indisponível")
#Validando o Ticker
if tickerChosen:
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

    tabs = st.tabs(["Evolução de preços", "Dividendos e Descobramentos", "Informações Gerais", "Indicadores Técnicos", "FAQ"])

    # Tab 1
    with tabs[0]:
        # Convertendo pandas Timestamps para objetos datetime do Python
        min_date = ticker_data.index.min().to_pydatetime()
        max_date = ticker_data.index.max().to_pydatetime()
        # Permitindo que o usuário selecione um intervalo de tempo
        st.subheader('Gráfico de evolução')
        from_date, to_date = st.slider(
        '📈Evolução da ação ao longo dos anos',
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
            try: 
                dividendYeld = tickerChosen.info['dividendYield']
            except:
                dividendYeld = None
            if dividendYeld:
                st.write(f"💰 Dividend Yield: {dividendYeld}")
            else:
                st.write(f"💰 Dividend Yield: Não informado")
        with col2:
            try: 
                dividendRate = tickerChosen.info['dividendRate']
            except:
                dividendRate = None
            if dividendRate:
                st.write(f"💰 Dividend Rate: {dividendRate}")
            else:
                st.write(f"💰 Dividend Rate: Não informado")
        st.subheader('💰 Dividendos Pagos anualmente')
        dividendsYearly = tickerChosen.dividends.resample('Y').sum()
        st.bar_chart(dividendsYearly)
        st.subheader('🔀Desdobramento das ações')
        st.dataframe(tickerChosen.splits)

    # Tab 3
    with tabs[2]:
        # Exbir informações contábeis
        st.subheader('📜 Informações Contábeis')
        st.dataframe(tickerChosen.financials )
        st.download_button('Download CSV Contábil', tickerChosen.financials.to_csv(), file_name='financeiro.csv')
        st.subheader('💵 Informações de Caixa')
        st.dataframe(tickerChosen.cashflow)
        st.download_button('Download CSV Caixa', tickerChosen.cash_flow.to_csv(), file_name='caixa.csv')

    #Tab 4
    with tabs[3]:
        #definindo um histórico de tempo menor para visualização otimizada
        smallData = tickerChosen.history(period="3y", interval="1d")
        # informações técnicas
        smallData['SMA_50'] = smallData['Close'].rolling(window=50).mean()
        smallData['SMA_200'] = smallData['Close'].rolling(window=200).mean()
        smallData['EMA_50'] = smallData['Close'].ewm(span=50, adjust=False).mean()
        # Adicionando os cálculos ao dataframe
        smallData['RSI'] = calculate_rsi(smallData['Close'])
        smallData['MACD'], smallData['Signal'] = calculate_macd(smallData['Close'])

        # Gráfico com Médias Móveis
        col1, col2, col3= st.columns([1,1,1])
        ''
        ''
        with col1:
            st.write(f"📈 **P/E Ratio:** {tickerChosen.info.get('trailingPE', 'N/A')}")
        with col2:
            st.write(f"📊 **P/B Ratio:** {tickerChosen.info.get('priceToBook', 'N/A')}")
        with col3:
            st.write(f"🏦 **ROE:** {tickerChosen.info.get('returnOnEquity', 'N/A')}")
        st.subheader('Evolução da Ação com Médias Móveis')
        st.line_chart(smallData[['Close', 'SMA_50', 'SMA_200']])
        st.subheader('📊 RSI - Índice de Força Relativa')
        st.line_chart(smallData[['RSI']])
        st.subheader('📈 MACD - Moving Average Convergence Divergence')
        st.line_chart(smallData[['MACD', 'Signal']])
        st.subheader('Múltiplos Financeiros')
    #Tab 5
    with tabs[4]:
        st.header("📖 FAQ Financeiro - Termos Explicados")
        with st.expander("📈 O que é o P/E Ratio? (Preço sobre Lucro)"):
            st.write(
            "O P/E Ratio (Price-to-Earnings Ratio) é um indicador que mostra "
            "quanto os investidores estão dispostos a pagar por cada dólar de lucro da empresa. "
            "Ele é calculado dividindo o preço da ação pelo lucro por ação (EPS)."
        )
        with st.expander("📊 O que significa o P/B Ratio? (Preço sobre Valor Patrimonial)"):
            st.write(
            "O P/B Ratio (Price-to-Book Ratio) compara o preço da ação com seu valor patrimonial por ação. "
            "Se for maior que 1, significa que o mercado valoriza a empresa acima do seu patrimônio líquido."
        )
        with st.expander("🏦 O que é o ROE? (Retorno sobre o Patrimônio)"):
            st.write(
            "O ROE (Return on Equity) mede a rentabilidade de uma empresa em relação ao seu patrimônio líquido. "
            "Ele indica o quão eficiente a empresa é em gerar lucro com seus próprios recursos."
        )

        with st.expander("💰 O que é Dividend Yield?"):
            st.write(
            "O Dividend Yield mostra o retorno em dividendos que um investidor recebe sobre o preço atual da ação. "
            "É calculado dividindo o dividendo anual pago pela empresa pelo preço da ação."
        )

        with st.expander("📉 O que é MACD? (Moving Average Convergence Divergence)"):
            st.write(
            "O MACD é um indicador técnico que ajuda a identificar mudanças na tendência do preço de um ativo. "
            "Ele compara duas médias móveis (geralmente de 12 e 26 períodos) e gera um sinal de compra ou venda."
        )

        with st.expander("📊 O que é RSI? (Índice de Força Relativa)"):
            st.write(
            "O RSI (Relative Strength Index) mede a velocidade e a mudança dos movimentos de preço. "
            "Ele varia entre 0 e 100, sendo que valores acima de 70 indicam sobrecompra e abaixo de 30 indicam sobrevenda."
        )
        with st.expander("📊 O que é a Evolução da Ação com Médias Móveis?"):
            st.write(
            "A evolução da ação com médias móveis exibe o preço de fechamento do ativo ao longo do tempo, "
            "juntamente com duas médias móveis: SMA (Simples) e EMA (Exponencial). "
            "Essas médias ajudam a identificar tendências e possíveis pontos de compra e venda."
        )

        with st.expander("📜 O que são informações contábeis?"):
            st.write(
            "As informações contábeis exibem os demonstrativos financeiros da empresa, como "
            "Receita, Lucro Bruto, EBITDA e outras métricas contábeis importantes. "
            "É útil para analisar a saúde financeira da empresa ao longo do tempo."
        )

        with st.expander("💵 O que são as informações de Caixa?"):
            st.write(
            "As informações de caixa mostram o fluxo de caixa da empresa, incluindo as entradas e saídas de dinheiro de diferentes fontes. "
            "Essa informação é essencial para entender se a empresa está gerando dinheiro suficiente para cobrir suas despesas."
        )

        with st.expander("🔀 O que significa Desdobramento das Ações?"):
            st.write(
            "O desdobramento de ações (stock split) ocorre quando uma empresa divide suas ações existentes "
            "em múltiplas ações novas, reduzindo o preço por ação sem alterar o valor total investido. "
            "Isso pode aumentar a liquidez do papel e torná-lo mais acessível para investidores."
        )
