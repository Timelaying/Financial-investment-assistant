import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier


class Portfolio:
    def __init__(self):
        self.weights = None
        self.transactions = pd.DataFrame(columns=["Date", "Type", "Asset", "Quantity", "Price"])
        self.portfolio_values = []

    def add_transaction(self, date, transaction_type, asset, quantity, price):
        try:
            date = pd.to_datetime(date)
            if pd.isnull(date):
                raise ValueError("Invalid date")
            quantity = float(quantity)
            price = float(price)
        except (ValueError, TypeError):
            st.warning("Invalid transaction data. Please check your input.")
            return

        new_transaction = pd.DataFrame({
            "Date": [date],
            "Type": [transaction_type],
            "Asset": [asset],
            "Quantity": [quantity],
            "Price": [price]
        })

        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        self.portfolio_values.append(self.portfolio_value())

    def clear_transaction_history(self):
        self.transactions = pd.DataFrame(columns=["Date", "Type", "Asset", "Quantity", "Price"])
        self.portfolio_values = []

    def portfolio_value(self):
        return (self.transactions["Quantity"] * self.transactions["Price"]).sum()

    def get_asset_percentage(self):
        if self.transactions.empty:
            return None

        asset_percentage = self.transactions.groupby('Asset').apply(lambda x: (x['Quantity'] * x['Price']).sum() / self.portfolio_value() * 100)
        return asset_percentage

    def plot_asset_percentage(self):
        asset_percentage = self.get_asset_percentage()
        if asset_percentage is None:
            return None

        labels = asset_percentage.index.tolist()
        values = asset_percentage.values.tolist()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Asset Allocation')
        return fig
    
    def calculate_weights(self):
        if self.transactions.empty:
            return None

        asset_percentage = self.get_asset_percentage()
        if asset_percentage is None:
            return None

        total_assets = len(asset_percentage)
        self.weights = asset_percentage / 100
        return self.weights

    def plot_portfolio_performance(self):
        if not self.portfolio_values:
            return None  # Return None if no portfolio values are available

        # Create a line chart showing portfolio value over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.transactions['Date'], y=self.portfolio_values, mode='lines', name='Portfolio Value'))
        fig.update_layout(title='Portfolio Performance',
                          xaxis_title='Date',
                          yaxis_title='Portfolio Value')

        return fig

    def transaction_history(self):
        return self.transactions


def portfolio_management():
    st.title("Portfolio Management")

    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = Portfolio()

    st.subheader("Add Transaction")
    date = st.date_input("Date", value=datetime.today())
    transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
    asset = st.text_input("Asset")
    quantity = st.number_input("Quantity", min_value=0)
    price = st.number_input("Price", min_value=0.01)
    if st.button("Add Transaction"):
        st.session_state.portfolio.add_transaction(date, transaction_type, asset, quantity, price)
        st.success("Transaction added successfully.")

    st.subheader("Portfolio Overview")
    portfolio_value = st.session_state.portfolio.portfolio_value()
    st.write(f"Portfolio Value: ${portfolio_value:.2f}")

    st.subheader("Asset Allocation")
    asset_percentage_chart = st.session_state.portfolio.plot_asset_percentage()
    if asset_percentage_chart is not None:
        st.plotly_chart(asset_percentage_chart)

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

