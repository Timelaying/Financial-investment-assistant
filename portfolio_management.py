import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

class Portfolio:
    def __init__(self):
        self.transactions = []
        self.portfolio_values = []

    def add_transaction(self, username, date_str, transaction_type, asset, quantity, price):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            quantity = float(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive.")
        except ValueError as e:
            st.warning(f"Invalid transaction data: {e}")
            return

        if transaction_type == "Sell":
            total_quantity = sum(trans["Quantity"] for trans in self.transactions if trans["Asset"] == asset)
            if total_quantity <= 0:
                st.warning(f"The asset '{asset}' does not exist in the portfolio for selling.")
                return
            if quantity > total_quantity:
                st.warning(f"Quantity to sell ({quantity}) exceeds available quantity ({total_quantity}) for asset '{asset}'.")
                return
            quantity *= -1

        transaction = {"Username": username, "Date": date_str, "Type": transaction_type, "Asset": asset, "Quantity": quantity, "Price": price}
        self.transactions.append(transaction)
        self.portfolio_values.append(self.portfolio_value())

        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM portfolios WHERE username=? AND asset=? AND quantity=? AND price=? AND date=?",
                       (username, asset, quantity, price, date_str))
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO portfolios (username, asset, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
                           (username, asset, quantity, price, date_str))
            conn.commit()
        conn.close()

    def portfolio_value(self):
        return sum(trans["Quantity"] * trans["Price"] for trans in self.transactions)

    def get_asset_percentage(self):
        if not self.transactions:
            return None
        assets = pd.DataFrame(self.transactions)
        asset_percentage = assets.groupby('Asset').apply(lambda x: (x['Quantity'] * x['Price']).sum() / self.portfolio_value() * 100)
        return asset_percentage

    def calculate_weights(self):
        if not self.transactions:
            return None
        asset_percentage = self.get_asset_percentage()
        if asset_percentage is None:
            return None
        weights = asset_percentage / 100
        return weights

    def plot_portfolio_performance(self):
        if not self.portfolio_values:
            return None
        dates = [trans['Date'] for trans in self.transactions]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=self.portfolio_values, mode='lines', name='Portfolio Value'))
        fig.update_layout(title='Portfolio Performance', xaxis_title='Date', yaxis_title='Portfolio Value')
        return fig

    def transaction_history(self):
        return pd.DataFrame(self.transactions)

def portfolio_management(username):
    st.title("Portfolio Management")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio()
    
    if not getattr(st.session_state, 'portfolio_initialized', False):
        load_user_data(username)
    
    st.subheader("Add Transaction")
    date_str = st.text_input("Date (YYYY-MM-DD)", value=datetime.today().strftime('%Y-%m-%d'))
    transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
    
    if transaction_type == "Sell":
        assets = list(set(trans["Asset"] for trans in st.session_state.portfolio.transactions if trans["Quantity"] > 0))
        asset = st.selectbox("Asset", assets)
    else:
        asset = st.text_input("Asset")
    
    quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
    price = st.number_input("Price", min_value=0.01, step=0.01)

    if st.button("Add Transaction"):
        st.session_state.portfolio.add_transaction(username, date_str, transaction_type, asset, quantity, price)
        load_user_data(username)
        st.success("Transaction added successfully.")

    st.subheader("Portfolio Overview")
    portfolio_value = st.session_state.portfolio.portfolio_value()
    st.write(f"Portfolio Value: ${portfolio_value:.2f}")

    st.subheader("Asset Allocation")
    asset_percentage_chart = st.session_state.portfolio.get_asset_percentage()
    if asset_percentage_chart is not None:
        st.bar_chart(asset_percentage_chart)

    if st.button("Calculate Weights"):
        weights = st.session_state.portfolio.calculate_weights()
        if weights is not None:
            st.write("Portfolio Weights:")
            st.write(weights)

    st.subheader("Portfolio Performance")
    performance_chart = st.session_state.portfolio.plot_portfolio_performance()
    if performance_chart is not None:
        st.plotly_chart(performance_chart)

    st.subheader("Transaction History")
    transaction_history = st.session_state.portfolio.transaction_history()
    st.write(transaction_history)

def load_user_data(username):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolios WHERE username=?", (username,))
    rows = cursor.fetchall()
    for row in rows:
        _, _, asset, quantity, price, date_str = row
        transaction_type = 'Buy' if quantity > 0 else 'Sell'
        if transaction_type == 'Sell':
            quantity = abs(quantity)
        st.session_state.portfolio.add_transaction(username, date_str, transaction_type, asset, quantity, price)
    conn.close()
    st.session_state.portfolio_initialized = True

portfolio_management("username")
