import streamlit as st
import numpy as np
import plotly.graph_objs as go
import yfinance as yf

class TradingSimulator:
    def __init__(self):
        pass

    def generate_price_data(self, num_days, volatility, data_source):
        """Generate simulated or historical price data."""
        if data_source == 'historical':
            data = yf.download("AAPL", period="1y")
            price_data = data['Close'].to_numpy()
        else:
            trend = np.sin(np.linspace(0, 10, num_days)) * 10
            noise = np.random.normal(0, volatility, num_days)
            price_data = np.cumsum(trend + noise) + 100  # Base price
        return price_data

    def simulate_trades(self, price_data, initial_balance):
        """Simulate trades based on a simple trading strategy."""
        balance = initial_balance
        buy_signal = True

        for i in range(1, len(price_data)):
            if price_data[i] > price_data[i - 1] and buy_signal:
                shares = balance / price_data[i]
                balance = 0
                buy_signal = False
            elif price_data[i] < price_data[i - 1] and not buy_signal:
                balance = shares * price_data[i]
                buy_signal = True

        return balance

    def candlestick_chart(self, price_data):
        """Generate a candlestick chart with price data."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.arange(len(price_data)), y=price_data, mode='lines', name='Price'))
        fig.add_trace(go.Candlestick(x=np.arange(len(price_data)),
                                      open=price_data,
                                      high=price_data + 2 * np.random.rand(len(price_data)),
                                      low=price_data - 2 * np.random.rand(len(price_data)),
                                      close=price_data,
                                      name='Candlestick'))
        fig.update_layout(title='Simulated Market Data (Candlestick Chart)',
                          xaxis_title='Days',
                          yaxis_title='Price',
                          xaxis_rangeslider_visible=False)
        return fig

def render_trading_simulator():
    st.title('Trading Simulator')

    # User input
    st.header('Parameters')
    num_days = st.slider('Number of Days', min_value=10, max_value=1000, value=100)
    volatility = st.slider('Volatility', min_value=0.01, max_value=0.10, value=0.02)
    initial_balance = st.number_input("Initial Balance ($)", min_value=1, step=1, value=10000)
    data_source = st.selectbox('Data Source', ['simulated', 'historical'])
    if data_source == 'historical':
        st.warning("Using historical data from Yahoo Finance.")

    # Initialize simulator and simulate market
    simulator = TradingSimulator()
    price_data = simulator.generate_price_data(num_days, volatility, data_source)

    # Candlestick chart
    st.subheader('Candlestick Chart')
    candlestick_chart = simulator.candlestick_chart(price_data)
    st.plotly_chart(candlestick_chart)

    # Display balance
    final_balance = simulator.simulate_trades(price_data, initial_balance)
    st.write(f"Initial Balance: ${initial_balance:.2f}")
    st.write(f"Final Balance: ${final_balance:.2f}")

