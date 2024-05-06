import numpy as np
import pytest
import sys
import os
from unittest.mock import patch, MagicMock


# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import utils
from trading_simulator import *

@pytest.fixture
def simulator():
    return TradingSimulator()

def test_generate_price_data(simulator):
    # Test simulated data generation
    num_days = 100
    volatility = 0.02
    data_source = 'simulated'
    price_data = simulator.generate_price_data(num_days, volatility, data_source)
    assert len(price_data) == num_days

    # Test historical data generation for 1 year period
    data_source = 'historical'
    period = "1y"
    num_days = 252  # Number of trading days in a year
    price_data = simulator.generate_price_data(num_days, volatility, data_source, period)
    assert len(price_data) == num_days

    # # Test historical data generation for 2 year period
    # period = "2y"
    # num_days = 2 * 252  # Number of trading days in 2 years
    # price_data = simulator.generate_price_data(num_days, volatility, data_source, period)
    # assert len(price_data) == num_days

    # # Test historical data generation for 5 year period
    # period = "5y"
    # num_days = 5 * 252  # Number of trading days in 5 years
    # price_data = simulator.generate_price_data(num_days, volatility, data_source, period)
    # assert len(price_data) == num_days


def test_simulate_trades(simulator):
    # Test with simulated price data
    price_data = np.array([100, 105, 110, 115, 120, 115, 110, 105])
    initial_balance = 1000
    final_balance = simulator.simulate_trades(price_data, initial_balance)
    assert final_balance > 0

    # Test with empty price data
    price_data = np.array([])
    final_balance = simulator.simulate_trades(price_data, initial_balance)
    assert final_balance == initial_balance

def test_candlestick_chart(simulator):
    # Test candlestick chart generation
    price_data = np.array([100, 105, 110, 115, 120, 115, 110, 105])
    candlestick_chart = simulator.candlestick_chart(price_data)
    assert candlestick_chart is not None

    # Add more specific tests for chart properties or data visualization if needed

def test_render_trading_simulator():
    # Since this function mainly consists of Streamlit interactions, it's challenging to write unit tests for it.
    # It's typically tested manually or using end-to-end testing frameworks like Selenium.
    pass
