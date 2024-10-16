import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime as dt

CRYPTO_NAME = 'BTC-USD'
START_DATE = '2024-01-01'

def fetch_crypto_data(crypto_name, start_date, end_date):
    try:
        data = yf.download(crypto_name, start=start_date, end=end_date)
        if data.empty:
            raise ValueError("No data fetched for the given date range.")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_candlestick_chart(data):
    candlestick = go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlesticks',
        increasing_line_color='blue',
        decreasing_line_color='grey'
    )
    return candlestick

def create_moving_average_chart(data, window=30):
    moving_average = go.Scatter(
        x=data.index,
        y=data['Close'].rolling(window=window).mean(),
        name=f'{window} Day Moving Average',
        mode='lines'
    )
    return moving_average

def plot_crypto_data(data):
    candlestick = create_candlestick_chart(data)
    moving_average = create_moving_average_chart(data)

    graph = go.Figure(data=[candlestick, moving_average])
    graph.update_layout(title='Lakshya Crypto Price Graph Analysis', yaxis_title='Price (USD)')
    graph.show()

def run():
    end_date = dt.now().strftime("%Y-%m-%d")
    crypto_data = fetch_crypto_data(CRYPTO_NAME, START_DATE, end_date)
    
    if crypto_data is not None:
        plot_crypto_data(crypto_data)

if __name__ == "__main__":
    run()
