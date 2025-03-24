# Importing the library which will be used to get the data from
import yfinance as yf


# Function to get an element of a company's income statement
def get_element_income_statement(ticker_symbol, element):
    company_data = yf.Ticker(ticker_symbol)
    income_statement = company_data.income_stmt
    result_element = income_statement.loc[element].values[0]

    return result_element


# Function to get an element of a company's cash flow
def get_element_cash_flow(ticker_symbol, element):
    company_data = yf.Ticker(ticker_symbol)
    cash_flow_statement = company_data.cash_flow
    result_element = cash_flow_statement.loc[element].values[0]

    return result_element


# Function to get an element of a company's balance sheet
def get_element_balance_sheet(ticker_symbol, element):
    company_data = yf.Ticker(ticker_symbol)
    cash_flow_statement = company_data.balance_sheet
    result_element = cash_flow_statement.loc[element].values[0]

    return result_element


# Get the first trading day of a stock
def get_ipo_date(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    history = stock_data.history(period="max").tz_localize(None)
    first_trading_date = history.index[0].date()

    return first_trading_date


# Get daily return of a stock
def get_daily_returns(ticker_symbol, date):
    historical_data = yf.download(ticker_symbol, date, end="2024-03-31")
    daily_returns = historical_data['Adj Close'].pct_change()

    return daily_returns.dropna()


# Get today's value
def get_today_value(ticker_symbol):
    bovespa_data = yf.Ticker(ticker_symbol)
    today_price = bovespa_data.history(period="1d")["Close"].iloc[-1]

    return today_price


# Get the number of stocks in the company
def get_total_outstanding_shares(ticker_symbol):
    stock_data = yf.Ticker(ticker_symbol)
    company_profile = stock_data.info

    total_shares_outstanding = company_profile.get('sharesOutstanding', None)

    return total_shares_outstanding
