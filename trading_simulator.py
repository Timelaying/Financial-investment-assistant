import streamlit as st
import numpy as np
import plotly.graph_objs as go
import yfinance as yf

class TradingSimulator:
    def __init__(self):
        self.num_days = 100
        self.base_price = 100
        self.volatility = 0.02
        self.strategy = 'simple'  # Default trading strategy
        self.data_source = 'simulated'  # Default data source

    def generate_price_data(self):
        """Generate simulated or historical price data."""
        if self.data_source == 'historical':
            # Download historical data from Yahoo Finance
            data = yf.download("AAPL", period="1y")
            price_data = data['Close'].to_numpy()
        else:
            # Simulate price data
            trend = np.sin(np.linspace(0, 10, self.num_days)) * 10
            noise = np.random.normal(0, self.volatility, self.num_days)
            price_data = np.cumsum(trend + noise) + self.base_price
        return price_data

    def simulate_trades(self, price_data, initial_balance):
        """Simulate trades based on the selected trading strategy."""
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

    # Parameters directly in the main display
    st.header('Parameters')
    num_days = st.slider('Number of Days', min_value=10, max_value=1000, value=100)
    volatility = st.slider('Volatility', min_value=0.01, max_value=0.10, value=0.02)
    initial_balance = st.number_input("Initial Balance ($)", min_value=1, step=1, value=10000)
    strategy = st.selectbox('Trading Strategy', ['simple', 'historical'])
    if strategy == 'historical':
        st.warning("Using historical data from Yahoo Finance.")

    # Initialize TradingSimulator
    simulator = TradingSimulator()
    simulator.num_days = num_days
    simulator.volatility = volatility
    simulator.strategy = strategy

    # Simulate market
    price_data = simulator.generate_price_data()

    # Candlestick chart
    st.subheader('Candlestick Chart')
    candlestick_chart = simulator.candlestick_chart(price_data)
    st.plotly_chart(candlestick_chart)

    # Display balance
    final_balance = simulator.simulate_trades(price_data, initial_balance)
    st.write(f"Initial Balance: ${initial_balance:.2f}")
    st.write(f"Final Balance: ${final_balance:.2f}")


