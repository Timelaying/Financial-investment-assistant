import pytest  # Importing pytest for testing
import sys  # Importing sys for system-specific parameters and functions
import os  # Importing os for operating system dependent functionality
import sqlite3  # Importing sqlite3 for SQLite database operations

# Add parent directory to sys.path to ensure modules in the parent directory can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import custom module 'portfolio_management' from the parent directory
from portfolio_management import *


# Mock for st.session_state
class MockSessionState:
    def __init__(self):
        self.portfolio = Portfolio()

@pytest.fixture
def empty_portfolio(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE portfolios
                      (username text, asset text, quantity real, price real, date text)''')
    conn.commit()
    conn.close()
    
    monkeypatch.setattr("streamlit.session_state", MockSessionState())

    portfolio = Portfolio()
    return portfolio, db_path

def test_portfolio_init(empty_portfolio):
    portfolio, _ = empty_portfolio
    assert isinstance(portfolio, Portfolio)
    assert len(portfolio.transactions) == 0
    assert len(portfolio.portfolio_values) == 0

def test_add_transaction(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    assert len(portfolio.transactions) == 1
    assert len(portfolio.portfolio_values) == 1

def test_add_sell_transaction(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Sell", "StockA", 5, 100)
    assert len(portfolio.transactions) == 2
    assert portfolio.transactions[-1]['Quantity'] == -5

def test_add_sell_transaction_insufficient_quantity(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Sell", "StockA", 15, 100)
    assert len(portfolio.transactions) == 1  # The second transaction should not be added

def test_portfolio_value(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    assert portfolio.portfolio_value() == 2000  # (10*100) + (20*50)

def test_get_asset_percentage(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    asset_percentage = portfolio.get_asset_percentage()
    assert asset_percentage is not None
    assert asset_percentage["StockA"] == 50.0  # (10*100)/(10*100 + 20*50)
    assert asset_percentage["StockB"] == 50.0  # (20*50)/(10*100 + 20*50)

def test_calculate_weights(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    weights = portfolio.calculate_weights()
    assert weights is not None
    assert weights["StockA"] == 0.5
    assert weights["StockB"] == 0.5

def test_transaction_history(empty_portfolio):
    portfolio, _ = empty_portfolio
    portfolio.add_transaction("user1", "2024-01-01", "Buy", "StockA", 10, 100)
    portfolio.add_transaction("user1", "2024-02-01", "Buy", "StockB", 20, 50)
    transaction_history = portfolio.transaction_history()
    assert len(transaction_history) == 2
    assert set(transaction_history.columns) == {'Username', 'Date', 'Type', 'Asset', 'Quantity', 'Price'}

def test_load_user_data(tmp_path):
    db_path = tmp_path / 'test.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE portfolios
                      (username text, asset text, quantity real, price real, date text)''')
    cursor.execute("INSERT INTO portfolios (username, asset, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
                   ("user1", "StockA", 10, 100, "2024-01-01"))
    cursor.execute("INSERT INTO portfolios (username, asset, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
                   ("user1", "StockB", 20, 50, "2024-02-01"))
    conn.commit()
    conn.close()

    # Mock for st.session_state
    class MockSessionState:
        def __init__(self):
            self.portfolio = Portfolio()

    # Initialize session state with portfolio
    st.session_state = MockSessionState()

    # Load user data
    load_user_data("user1")

    # Now make assertions based on the loaded data
    assert len(st.session_state.portfolio.transactions) == 3
    assert st.session_state.portfolio.transactions[0]["Asset"] == "StockA"
    assert st.session_state.portfolio.transactions[1]["Asset"] == "StockA"
    assert st.session_state.portfolio.transactions[2]["Asset"] == "StockB"

