# Import necessary libraries
import streamlit as st
import json
import sqlite3
from widgets import __login__

# Modules for tabs
from news_in import main_news
from realtime_stock_monitoring import render_realtime_stock_monitoring
from trading_simulator import render_trading_simulator
from reading_resources import render_reading_resources
from recommendation_results import generate_recommendation_results
from portfolio_management import portfolio_management

# Authenticate user
__login__obj = __login__(
    # auth_token="pk_prod_0PP3FYA7VXMJ3EKZNB7R7SKWFWHR",  # st.secrets.email_api_key
    company_name="Finance Adviser",
    width=200, height=250,
    logout_button_name='Logout', hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')
LOGGED_IN = __login__obj.build_login_ui()

# Main application logic
if LOGGED_IN:

    # Initialize session state
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'risk_tolerance': 'High',
            'investment_horizon': 'Short-term - 1 to 3 years',
            'investment_style': 'Value Investing'
        }

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
    cursor.executemany("INSERT OR IGNORE INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
                    [(user['username'], user['name'], user['email'], user['password']) for user in credentials])
    
    #table for portfolio
    cursor.execute('''CREATE TABLE IF NOT EXISTS portfolios
                               (id INTEGER PRIMARY KEY, 
                                username TEXT, 
                                asset TEXT, 
                                quantity REAL, 
                                price REAL, 
                                date DATE)''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Get username from login
    username = __login__obj.get_username()


    # Display tabs and selected stock data
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        'New',
        'Market analysis',
        'Trading simulator',
        'Reading resources',
        'Recommendation',
        'Management of portfolio'])
    
    with tab1:
        main_news()
        
    with tab2:
        
        render_realtime_stock_monitoring()

    with tab3:
        render_trading_simulator()

    with tab4:
        render_reading_resources()

    with tab5:
        generate_recommendation_results()

    with tab6:
        portfolio_management(username)

else:
    st.warning("Please log in to access Finance Adviser.")
