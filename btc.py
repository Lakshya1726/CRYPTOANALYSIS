import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime as dt

# Constant for the cryptocurrency name
CRYPTO_NAME = 'BTC-USD'

def get_data(crypto_name=CRYPTO_NAME, start_date='2024-01-01', end_date=None):
    """
    Fetches historical cryptocurrency data using yfinance.

    Parameters:
    crypto_name (str): The symbol for the cryptocurrency (default is 'BTC-USD').
    start_date (str): The start date for fetching data (default is '2024-01-01').
    end_date (str): The end date for fetching data (default is today's date).

    Returns:
    pandas.DataFrame: Historical data for the specified cryptocurrency.
    """
    # Get today's date if not provided
    if end_date is None:
        end_date = dt.now().strftime("%Y-%m-%d")
    
    # Error handling for data fetch
    try:
        data = yf.download(crypto_name, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"No data found for {crypto_name} in the specified date range.")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_crypto_chart(data, crypto_name=CRYPTO_NAME):
    """
    Creates and displays a candlestick chart with a 30-day moving average.

    Parameters:
    data (pandas.DataFrame): Historical cryptocurrency data.
    crypto_name (str): The symbol for the cryptocurrency (default is 'BTC-USD').
    """
    if data is None:
        print("No data to plot.")
        return

    # Create the candlestick and moving average chart
    graph = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=f'{crypto_name} Candlestick',
            increasing_line_color='blue',
            decreasing_line_color='grey'
        ),
        go.Scatter(
            x=data.index,
            y=data['Close'].rolling(window=30).mean(),
            name='30 Day Moving Average',
            mode='lines'
        )
    ])

    # Update the layout for the chart
    graph.update_layout(
        title=f'{crypto_name} Price Analysis',
        yaxis_title='Price (USD)',
        xaxis_title='Date'
    )

    # Show the chart
    graph.show()

def run():
    """
    Main function to run the data fetching and chart plotting.
    """
    crypto_data = get_data()
    if crypto_data is not None:
        create_crypto_chart(crypto_data)

if __name__ == '__main__':
    run()
