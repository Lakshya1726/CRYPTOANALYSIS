from flask import Flask, render_template_string, request, send_file
import yfinance as yf
import plotly.graph_objects as go
import plotly
import json
import pandas as pd
from datetime import datetime as dt
import io

app = Flask(__name__)

# Default cryptocurrency and date range
DEFAULT_CRYPTO_NAME = 'BTC-USD'
DEFAULT_START_DATE = '2024-01-01'

def get_data(crypto_name, start_date, end_date):
    data = yf.download(crypto_name, start=start_date, end=end_date)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    crypto_name = DEFAULT_CRYPTO_NAME
    start_date = DEFAULT_START_DATE
    end_date = dt.now().strftime("%Y-%m-%d")

    if request.method == 'POST':
        crypto_name = request.form.get('crypto_name', DEFAULT_CRYPTO_NAME)
        start_date = request.form.get('start_date', DEFAULT_START_DATE)
        end_date = request.form.get('end_date', dt.now().strftime("%Y-%m-%d"))

    crypto_data = get_data(crypto_name, start_date, end_date)

    # Calculate additional indicators
    moving_avg_30 = crypto_data['Close'].rolling(window=30).mean()
    moving_avg_50 = crypto_data['Close'].rolling(window=50).mean()
    rsi = compute_rsi(crypto_data['Close'], 14)
    bollinger_upper, bollinger_lower = compute_bollinger_bands(crypto_data['Close'])
    macd, macd_signal = compute_macd(crypto_data['Close'])

    # Create candlestick chart data
    candlestick = go.Candlestick(
        x=crypto_data.index,
        open=crypto_data['Open'],
        high=crypto_data['High'],
        low=crypto_data['Low'],
        close=crypto_data['Close'],
        name='Candlesticks',
        increasing_line_color='cyan',
        decreasing_line_color='orange'
    )

    # Create moving average data
    moving_avg_30_line = go.Scatter(
        x=crypto_data.index,
        y=moving_avg_30,
        name='30 Day Moving Average',
        mode='lines',
        line=dict(color='lightgreen', width=2)
    )
    
    moving_avg_50_line = go.Scatter(
        x=crypto_data.index,
        y=moving_avg_50,
        name='50 Day Moving Average',
        mode='lines',
        line=dict(color='gold', width=2)
    )

    # Create Bollinger Bands
    bollinger_upper_line = go.Scatter(
        x=crypto_data.index,
        y=bollinger_upper,
        name='Bollinger Upper Band',
        mode='lines',
        line=dict(color='red', width=1, dash='dash')
    )
    
    bollinger_lower_line = go.Scatter(
        x=crypto_data.index,
        y=bollinger_lower,
        name='Bollinger Lower Band',
        mode='lines',
        line=dict(color='blue', width=1, dash='dash')
    )

    # Create MACD data
    macd_line = go.Scatter(
        x=crypto_data.index,
        y=macd,
        name='MACD',
        mode='lines',
        line=dict(color='purple', width=2)
    )
    
    macd_signal_line = go.Scatter(
        x=crypto_data.index,
        y=macd_signal,
        name='MACD Signal',
        mode='lines',
        line=dict(color='orange', width=2)
    )

    # Create figure
    fig = go.Figure(data=[
        candlestick,
        moving_avg_30_line,
        moving_avg_50_line,
        bollinger_upper_line,
        bollinger_lower_line,
        macd_line,
        macd_signal_line
    ])
    fig.update_layout(
        title=f'{crypto_name} Price Graph Analysis',
        yaxis_title='Price (USD)',
        template='plotly_white'
    )

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render HTML template
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crypto Price Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
                color: black;
                transition: background-color 0.3s, color 0.3s;
            }
            h1 {
                text-align: center;
            }
            .form-container {
                text-align: center;
                margin-bottom: 20px;
            }
            .input-field {
                margin: 5px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            .button {
                padding: 10px 20px;
                margin: 10px;
                cursor: pointer;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #0056b3;
            }
            .download-button {
                background-color: #28a745;
            }
            .download-button:hover {
                background-color: #218838;
            }
            .dark {
                background-color: #2c2c2c;
                color: white;
            }
            .dark .input-field {
                background-color: #3c3c3c;
                border: 1px solid #777;
            }
            .dark .button {
                background-color: #007bff;
            }
            .dark .button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body class="light" id="body">
        <h1>Crypto Price Analysis</h1>
        <div class="form-container">
            <form method="POST">
                <input type="text" class="input-field" name="crypto_name" placeholder="Cryptocurrency (e.g. BTC-USD)" required>
                <input type="date" class="input-field" name="start_date" value="{{ request.form['start_date'] }}">
                <input type="date" class="input-field" name="end_date" value="{{ request.form['end_date'] }}">
                <button type="submit" class="button">Update</button>
            </form>
            <button class="button download-button" onclick="downloadCSV()">Download Data as CSV</button>
            <button class="button" id="theme-button" onclick="toggleTheme()">Switch to Dark Mode</button>
        </div>
        <div id="chart"></div>

        <script>
            var graphDiv = document.getElementById('chart');
            var graphJSON = {{ graph_json | safe }};
            Plotly.newPlot(graphDiv, graphJSON.data, graphJSON.layout);

            function toggleTheme() {
                var body = document.getElementById('body');
                var themeButton = document.getElementById('theme-button');

                if (body.classList.contains('light')) {
                    body.classList.remove('light');
                    body.classList.add('dark');
                    themeButton.innerText = 'Switch to Light Mode';

                    // Set light background for the dark theme
                    Plotly.relayout(graphDiv, {
                        'paper_bgcolor': 'white',
                        'plot_bgcolor': 'white',
                        'font.color': 'black'
                    });
                } else {
                    body.classList.remove('dark');
                    body.classList.add('light');
                    themeButton.innerText = 'Switch to Dark Mode';

                    // Set dark background for the light theme
                    Plotly.relayout(graphDiv, {
                        'paper_bgcolor': 'black',
                        'plot_bgcolor': 'black',
                        'font.color': 'white'
                    });
                }
            }

            function downloadCSV() {
                window.location.href = '/download';
            }
        </script>
    </body>
    </html>
    ''', graph_json=graph_json)

@app.route('/download')
def download():
    crypto_data = get_data(DEFAULT_CRYPTO_NAME, DEFAULT_START_DATE, dt.now().strftime("%Y-%m-%d"))
    csv = crypto_data.to_csv()
    
    return send_file(io.BytesIO(csv.encode()), download_name='crypto_data.csv', as_attachment=True)

def compute_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_bollinger_bands(data, window=20):
    moving_avg = data.rolling(window=window).mean()
    std_dev = data.rolling(window=window).std()
    upper_band = moving_avg + (std_dev * 2)
    lower_band = moving_avg - (std_dev * 2)
    return upper_band, lower_band

def compute_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    macd_signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, macd_signal

if __name__ == '__main__':
    app.run(debug=True)
