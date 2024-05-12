import pytest
import sys
import os
import sqlite3

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import
from portfolio_management import *

@pytest.fixture
def empty_portfolio(tmp_path):
    # Create a temporary database for testing
    db_path = tmp_path / 'test.db'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    # Create the 'portfolios' table
    cursor.execute('''CREATE TABLE portfolios
                      (username text, asset text, quantity real, price real, date text)''')
    conn.commit()
    conn.close()
    return Portfolio()  # Initialize Portfolio without any arguments

def test_portfolio_init(empty_portfolio):
    # Test the initialization of Portfolio
    assert isinstance(empty_portfolio, Portfolio)
    assert len(empty_portfolio.transactions) == 0
    assert len(empty_portfolio.portfolio_values) == 0

def test_add_transaction(empty_portfolio):
    # Test adding a transaction to the portfolio
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    assert len(empty_portfolio.transactions) == 1
    assert len(empty_portfolio.portfolio_values) == 1

def test_portfolio_value(empty_portfolio):
    # Test calculating portfolio value
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    empty_portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    assert empty_portfolio.portfolio_value() == 2000  # (10*100) + (20*50)

def test_get_asset_percentage(empty_portfolio):
    # Test calculating asset percentage
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    empty_portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    asset_percentage = empty_portfolio.get_asset_percentage()
    assert asset_percentage is not None
    assert asset_percentage["StockA"] == 50.0  # (10*100)/(10*100 + 20*50)
    assert asset_percentage["StockB"] == 50.0  # (20*50)/(10*100 + 20*50)

def test_calculate_weights(empty_portfolio):
    # Test calculating portfolio weights
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    empty_portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    weights = empty_portfolio.calculate_weights()
    assert weights is not None
    assert weights["StockA"] == 0.5
    assert weights["StockB"] == 0.5

def test_plot_portfolio_performance(empty_portfolio):
    # Test plotting portfolio performance
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    empty_portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    performance_chart = empty_portfolio.plot_portfolio_performance()
    assert performance_chart is not None
    assert isinstance(performance_chart, go.Figure)

def test_transaction_history(empty_portfolio):
    # Test retrieving transaction history
    empty_portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    empty_portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    transaction_history = empty_portfolio.transaction_history()
    assert len(transaction_history) == 2
    assert set(transaction_history.columns) == {'Username', 'Date', 'Type', 'Asset', 'Quantity', 'Price'}