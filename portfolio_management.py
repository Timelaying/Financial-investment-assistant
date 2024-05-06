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
            quantity = float(quantity)
            price = float(price)
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive.")
        except ValueError:
            st.warning("Invalid transaction data. Please check your input.")
            return

        self.transactions.append({"Username": username, "Date": date_str, "Type": transaction_type, "Asset": asset, "Quantity": quantity, "Price": price})
        self.portfolio_values.append(self.portfolio_value())
        # Connect to database
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        # Insert transaction into database
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
    
    # Initialize portfolio
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio()
    
    # Retrieve existing portfolio data from the database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolios WHERE username=?", (username,))
    rows = cursor.fetchall()
    for row in rows:
        username_db, _, asset, quantity, price, date_str = row
        st.session_state.portfolio.add_transaction(username_db, date_str, 'Buy', asset, quantity, price)
    conn.close()
    
    # Display transaction interface
    st.subheader("Add Transaction")
    date_str = st.text_input("Date (YYYY-MM-DD)", value=datetime.today().strftime('%Y-%m-%d'))
    transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
    asset = st.text_input("Asset")
    quantity = st.number_input("Quantity", min_value=0)
    price = st.number_input("Price", min_value=0.01)

    if st.button("Add Transaction"):
        st.session_state.portfolio.add_transaction(username, date_str, transaction_type, asset, quantity, price)
        st.success("Transaction added successfully.")

    # Display portfolio overview, asset allocation, weights, performance, and transaction history as before
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
