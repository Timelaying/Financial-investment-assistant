import pytest
import sys
import os
from portfolio_management import Portfolio  # Replace `portfolio_management` with the actual module name

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import
from portfolio_management import *

@pytest.fixture
def empty_portfolio():
    return Portfolio()

@pytest.fixture
def sample_portfolio():
    portfolio = Portfolio()
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    return portfolio

def test_portfolio_init(empty_portfolio):
    assert empty_portfolio.transactions == []
    assert empty_portfolio.portfolio_values == []

def test_portfolio_add_transaction(empty_portfolio):
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    assert len(empty_portfolio.transactions) == 1
    assert len(empty_portfolio.portfolio_values) == 1

def test_portfolio_value(sample_portfolio):
    assert sample_portfolio.portfolio_value() == (10 * 100) + (20 * 50)

def test_get_asset_percentage(sample_portfolio):
    asset_percentage = sample_portfolio.get_asset_percentage()
    assert asset_percentage.loc["StockA"] == pytest.approx(((10 * 100) / ((10 * 100) + (20 * 50))) * 100)
    assert asset_percentage.loc["StockB"] == pytest.approx(((20 * 50) / ((10 * 100) + (20 * 50))) * 100)

def test_calculate_weights(sample_portfolio):
    weights = sample_portfolio.calculate_weights()
    assert weights.loc["StockA"] == pytest.approx(((10 * 100) / ((10 * 100) + (20 * 50))))
    assert weights.loc["StockB"] == pytest.approx(((20 * 50) / ((10 * 100) + (20 * 50))))


# Testing of plot_portfolio_performance() would be complex due to the involvement of Plotly, 
# which might not be straightforward to test with pytest.

# Testing of transaction_history() could involve comparing the returned DataFrame with expected data.

# Mocking Streamlit's session state and SQLite database would be necessary for testing portfolio_management().

