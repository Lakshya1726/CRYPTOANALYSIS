import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime as dt

CRYPTO_NAME = 'BTC-USD'

def get_data():
    start_date = '2024-01-01'
    end_date = dt.now().strftime("%Y-%m-%d")
 
    data = yf.download(CRYPTO_NAME, start=start_date, end=end_date)
    return data

def run():
    crypto_data = get_data()

    graph = go.Figure(data=[
        go.Candlestick(
            x=crypto_data.index,
            open=crypto_data['Open'],
            high=crypto_data['High'],
            low=crypto_data['Low'],
            close=crypto_data['Close'],
            name='Candlesticks',
            increasing_line_color='blue',
            decreasing_line_color='grey'
        ),
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data['Close'].rolling(window=30).mean(),
            name='30 Day Moving Average',
            mode='lines'
        )
    ])

    graph.update_layout(title='Lakshya Crypto Price Graph Analysis', yaxis_title='Price (USD)')
    graph.show()

run()