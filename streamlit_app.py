# Importando as bibliotecas a serem utilizadas
import streamlit as st
import pandas as pd
import yfinance as yf
import math

# Definindo o título e o ícone do aplicativo
st.set_page_config(
    page_title='Dashboard de Índices dos Mercados Financeiros',
    page_icon=':chart_with_upwards_trend:',
)


# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_index_data(indexes):
    """
    Fetch stock market index data using yfinance.

    Args:
        indexes (dict): A dictionary mapping country codes to stock market tickers.

    Returns:
        pd.DataFrame: A DataFrame containing stock index data.
    """
    # Fetch historical data for each index
    data_frames = []
    for country, ticker in indexes.items():
        stock_data = yf.download(ticker, period='10y', interval='1d')
        stock_data['Country Code'] = country
        stock_data.reset_index(inplace=True)
        data_frames.append(stock_data[['Date', 'Close', 'Country Code']])

    # Combine all data frames
    return pd.concat(data_frames, ignore_index=True)


# Definindo os índices dos principais mercados
INDEXES = {
    'DEU': '^GDAXI',  # Germany - DAX
    'FRA': '^FCHI',  # France - CAC 40
    'GBR': '^FTSE',  # United Kingdom - FTSE 100
    'BRA': '^BVSP',  # Brazil - IBOVESPA
    'MEX': '^MXX',  # Mexico - IPC
    'JPN': '^N225',  # Japan - Nikkei 225
}

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :chart_with_upwards_trend: Dashboard de Índices dos Mercados Financeiros

Explore os índices dos mercados financeiros dos principais países.
'''

# Add some spacing
''
''

# Rodando a função para pegar o histórico dos índices
index_data = get_index_data(INDEXES)

# Convertendo pandas Timestamps para Python datetime objects
min_date = index_data['Date'].min().to_pydatetime()
max_date = index_data['Date'].max().to_pydatetime()

from_date, to_date = st.slider(
    'Em que período de tempo você está interessado?',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

countries = list(INDEXES.keys())

if not len(countries):
    st.warning("Selecione ao menos um país")

selected_countries = st.multiselect(
    'Quais países deseja visualizar?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
)

''
''
''

# Filtrando os dados por país e data
filtered_index_data = index_data[
    (index_data['Country Code'].isin(selected_countries))
    & (index_data['Date'] <= to_date)
    & (from_date <= index_data['Date'])
    ]

st.header('Stock Market Index Over Time', divider='gray')

''

# Plotando os dados
st.line_chart(
    filtered_index_data,
    x='Date',
    y='Close',
    color='Country Code',
)

''
''

# Mostrando as métricas dos dados mostrados
st.header(f'Stock Market Index Metrics', divider='gray')

cols = st.columns(4)


def get_closest_date(data, target_date):
    """
    Find the closest date in the data to the target_date.

    Args:
        data (pd.DataFrame): The DataFrame containing a 'Date' column.
        target_date (datetime): The target date to match.

    Returns:
        datetime: The closest available trading date.
    """
    available_dates = data['Date']
    closest_date = available_dates.loc[(available_dates - target_date).abs().idxmin()]
    return closest_date


for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        # Filter data for the current country
        country_data = filtered_index_data[filtered_index_data['Country Code'] == country]

        if country_data.empty:
            # Handle empty data scenario gracefully
            st.write(f"No data available for {country} in the selected range.")
            continue

        # Find closest available dates for the range
        closest_start_date = get_closest_date(country_data, from_date)
        closest_end_date = get_closest_date(country_data, to_date)

        # Ensure that the dates exist in the data
        start_value = country_data[country_data['Date'] == closest_start_date]['Close']
        end_value = country_data[country_data['Date'] == closest_end_date]['Close']

        if start_value.empty or end_value.empty:
            st.write(f"Missing data for {country} in the selected range.")
            continue

        # Access the first value safely
        start_value = start_value.iat[0]
        end_value = end_value.iat[0]

        # Calculate growth
        if math.isnan(start_value) or math.isnan(end_value):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{end_value / start_value:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} Index',
            value=f'{end_value:,.0f}',
            delta=growth,
            delta_color=delta_color
        )
