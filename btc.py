import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime as dt
import pandas as pd

# Define the crypto asset to analyze
CRYPTO_NAME = 'BTC-USD'

# Function to get the cryptocurrency data from yfinance
def get_data(start_date, end_date):
    data = yf.download(CRYPTO_NAME, start=start_date, end=end_date)
    return data

# Main function to run the analysis and create the graph
def run():
    # Set start and end dates
    start_date = '2024-01-01'
    end_date = dt.now().strftime("%Y-%m-%d")

    # Fetch crypto data
    crypto_data = get_data(start_date, end_date)
    
    # Add a 60-day moving average to the data
    crypto_data['60_MA'] = crypto_data['Close'].rolling(window=60).mean()

    # Create the candlestick chart with volume bars
    graph = go.Figure(data=[
        # Candlestick chart
        go.Candlestick(
            x=crypto_data.index,
            open=crypto_data['Open'],
            high=crypto_data['High'],
            low=crypto_data['Low'],
            close=crypto_data['Close'],
            name='Candlesticks',
            increasing_line_color='blue',  # Color for upward movements
            decreasing_line_color='grey'  # Color for downward movements
        ),
        # 30-day moving average line
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data['Close'].rolling(window=30).mean(),
            name='30 Day Moving Average',
            mode='lines',
            line=dict(color='orange', width=2)
        ),
        # 60-day moving average line
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data['60_MA'],
            name='60 Day Moving Average',
            mode='lines',
            line=dict(color='green', width=2)
        ),
        # Volume bars
        go.Bar(
            x=crypto_data.index,
            y=crypto_data['Volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.3,
            yaxis='y2'  # Separate axis for volume
        )
    ])

    # Update the layout for better visualization
    graph.update_layout(
        title='Lakshya Crypto Price Graph Analysis with Volume and Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        yaxis2=dict(
            title='Volume', overlaying='y', side='right', showgrid=False
        ),
        xaxis_rangeslider_visible=False,  # Hide the range slider for a cleaner look
        template='plotly_dark'  # Dark theme for a professional appearance
    )

    # Show the graph
    graph.show()

# Run the function to display the graph
run()
