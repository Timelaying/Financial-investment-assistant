# Import necessary libraries
import streamlit as st
import json
import sqlite3
from widgets import __login__
from safe import render_safely

# Modules for tabs
from news_in import main_news
from realtime_stock_monitoring import render_realtime_stock_monitoring
from trading_simulator import render_trading_simulator
from reading_resources import render_reading_resources
from recommendation_results import generate_recommendation_results
from portfolio_management import portfolio_management

# Authenticate user
__login__obj = __login__(
    company_name="Financial Investment Assistant",
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
            'risk_tolerance': 'Medium',
            'investment_horizon': 'Short-term - 1 to 3 years',
            'investment_style': 'Growth Investing'
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
    
    # Table for portfolio
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
        'News',
        'Market analysis',
        'Trading simulator',
        'Reading resources',
        'Recommendation',
        'Management of portfolio'])
    
    with tab1:
        render_safely('News', main_news)
        
    with tab2:
        render_safely('Market analysis', render_realtime_stock_monitoring)
    
    with tab3:
        render_safely('The trading simulator', render_trading_simulator)
    
    with tab4:
        render_safely('Reading resources', render_reading_resources)
    
    with tab5:
        render_safely('Recommendations', generate_recommendation_results)
    
    with tab6:
        render_safely('Portfolio management', portfolio_management, username)

else:
    st.warning("Please log in to access Finance Adviser.")
