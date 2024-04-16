# Import necessary libraries
import requests
import pandas_ta
import pypfopt
import ta
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from streamlit_login_auth_ui.widgets import __login__
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier  #more resistant to over fitting
from pypfopt import EfficientFrontier, risk_models, expected_returns
import sqlite3
import json

# Modules for tabs
from news import render_news
from realtime_stock_monitoring import render_realtime_stock_monitoring
from trading_simulator import render_trading_simulator
from reading_resources import render_reading_resources
from recommendation_results import generate_recommendation_results
from portfolio_management import portfolio_management

# Set page configuration and header
st.set_page_config(page_title="Finance Adviser")
st.header("Finance Adviser")

# Load credentials from JSON file
with open('_secret_auth_.json') as f:
    credentials = json.load(f)

# Connect to SQLite database (create one if it doesn't exist)
conn = sqlite3.connect('credentials.db')
cursor = conn.cursor()

# Create a table to store credentials
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')

# Insert credentials into the table, checking for duplicates
for user in credentials:
    username = user['username']
    name = user['name']
    email = user['email']
    password = user['password']
    
    # Check if username or email already exists in the database
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone()[0] == 0:  # Username or email does not exist
        cursor.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
                       (username, name, email, password))
    else:
        st.error(f"The username '{username}' or email '{email}' already exists. Please choose a different one.")

# Commit changes and close connection
conn.commit()
conn.close()



# Authenticate user
__login__obj = __login__(
    auth_token="pk_prod_0PP3FYA7VXMJ3EKZNB7R7SKWFWHR",  # st.secrets.email_api_key
    company_name="Finance Adviser",
    width=200, height=250,
    logout_button_name='Logout', hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')
LOGGED_IN = __login__obj.build_login_ui()

# Main application logic
if LOGGED_IN:
    # Check if form data exists in session state
    if 'form_data' not in st.session_state:
        # Initialize session state to store form data
        st.session_state.form_data = {
            'goal': "",
            'option': [],
            'risk_tolerance': "",
            'investment_horizon': "",
            'investment_amount': 1000.0,
            'types_of_stocks': [],
            'investment_style': ""
        }

    # Use the stored form data to prefill form fields
    form_placeholder = st.empty()  # Create a placeholder for the form

    # Display the form only if it hasn't been submitted
    if not st.session_state.get('form_submitted', False):
        with form_placeholder.form("Question"):
            # Introduction
            st.write(
                """
                Welcome to the Portfolio Goals page! Here, you can define your investment objectives and preferences.
                Please fill out the following fields to help us tailor investment recommendations for you.
                """)

            # Goal
            st.subheader("Goal")
            st.session_state.form_data['goal'] = st.text_input("What is your investment goal?",
                                                                value=st.session_state.form_data['goal'], type="default")

            # Stocks of interest
            st.subheader("Stocks of interest")
            st.session_state.form_data['option'] = st.multiselect(
                'What stocks are you interested in?',
                ('Google', 'Apple', 'Nvidia'),
                default=st.session_state.form_data['option'])

            # Risk Tolerance
            st.subheader("Risk Tolerance")
            risk_tolerance_options = ["Low", "Medium", "High"]
            risk_tolerance_index = risk_tolerance_options.index(
                st.session_state.form_data['risk_tolerance']) if st.session_state.form_data[
                'risk_tolerance'] in risk_tolerance_options else 1
            st.session_state.form_data['risk_tolerance'] = st.selectbox(
                "Select your risk tolerance",
                risk_tolerance_options,
                index=risk_tolerance_index)

            # Investment horizon
            st.subheader("Investment Horizon")
            investment_horizon_options = ["Short-term - 1 to 3 years", "Medium-term - 3 to 5 years",
                                          "Long-term - 5 years or more"]
            investment_horizon_index = investment_horizon_options.index(
                st.session_state.form_data['investment_horizon']) if st.session_state.form_data[
                'investment_horizon'] in investment_horizon_options else 1
            st.session_state.form_data['investment_horizon'] = st.selectbox(
                "Select your investment horizon",
                investment_horizon_options,
                index=investment_horizon_index)

            # Investment amount
            st.subheader("Investment Amount")
            st.session_state.form_data['investment_amount'] = st.number_input(
                "Enter your investment amount ($)",
                min_value=0.0,
                step=100.0,
                value=st.session_state.form_data['investment_amount'])

            # Types of stocks
            st.subheader("Types of Stocks")
            st.session_state.form_data['types_of_stocks'] = st.multiselect(
                "Select types of stocks you're interested in",
                ["Technology", "Finance", "Healthcare", "Consumer Goods"],
                default=st.session_state.form_data['types_of_stocks'])

            # Investment style
            st.subheader("Investment Style")
            investment_style_options = ["Value Investing", "Growth Investing", "Index Investing"]
            investment_style_index = investment_style_options.index(
                st.session_state.form_data['investment_style']) if st.session_state.form_data[
                'investment_style'] in investment_style_options else 1
            st.session_state.form_data['investment_style'] = st.radio(
                "Select your investment style",
                investment_style_options,
                index=investment_style_index)

            submitted = st.form_submit_button("Submit")

        if submitted:
            # Hide the form after submission
            form_placeholder.empty()
            st.session_state.form_submitted = True

    # Display tabs and selected stock data
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        'New',
        'Market analysis',
        'Trading simulator',
        'Reading resources',
        'Recommendation',
        'Management of portfolio'])

    with tab1:
        render_news()

    with tab2:
        render_realtime_stock_monitoring()

    with tab3:
        render_trading_simulator()

    with tab4:
        render_reading_resources()

    with tab5:
        generate_recommendation_results()

    with tab6:
        portfolio_management()

else:
    st.warning("Please log in to access Finance Adviser.")
