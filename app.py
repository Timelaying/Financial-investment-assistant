import requests
import pandas as pd
import yfinance as yf
import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(page_title="Finance Adviser")
st.header("Finance Adviser")

__login__obj = __login__(
    auth_token="pk_prod_0PP3FYA7VXMJ3EKZNB7R7SKWFWHR",  # st.secrets.email_api_key
    company_name="Finance Adviser",
    width=200, height=250,
    logout_button_name='Logout', hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

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
            st.session_state.form_data['goal'] = st.text_input("What is your investment goal?", value=st.session_state.form_data['goal'], type="default")

            # Stocks of interest
            st.subheader("Stocks of interest")
            st.session_state.form_data['option'] = st.multiselect(
                'What stocks are you interested in?',
                ('Google', 'Apple', 'Nvidia'),
                default=st.session_state.form_data['option'])

            # Risk Tolerance
            st.subheader("Risk Tolerance")
            risk_tolerance_options = ["Low", "Medium", "High"]
            risk_tolerance_index = risk_tolerance_options.index(st.session_state.form_data['risk_tolerance']) if st.session_state.form_data['risk_tolerance'] in risk_tolerance_options else 1
            st.session_state.form_data['risk_tolerance'] = st.selectbox(
                "Select your risk tolerance",
                risk_tolerance_options,
                index=risk_tolerance_index)

            # Investment horizon
            st.subheader("Investment Horizon")
            investment_horizon_options = ["Short-term - 1 to 3 years", "Medium-term - 3 to 5 years", "Long-term - 5 years or more"]
            investment_horizon_index = investment_horizon_options.index(st.session_state.form_data['investment_horizon']) if st.session_state.form_data['investment_horizon'] in investment_horizon_options else 1
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
            investment_style_index = investment_style_options.index(st.session_state.form_data['investment_style']) if st.session_state.form_data['investment_style'] in investment_style_options else 1
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
        @st.cache_data
        def get_news():
            link_list = []
            headline_list = []
            url = 'https://www.cnbc.com/world-markets/'
            get_url = requests.get(url)
            soup = BeautifulSoup(get_url.text, "html.parser")
            links = [link.get('href') for link in soup.find_all('a')]
            links = [link for link in links if link and link.startswith('https://www.cnbc.com/2024/')]
            # Function to normalize URLs for comparison
            def normalize_url(url):
                parsed_url = urlparse(url)
                return parsed_url.geturl()

            links = list(set(normalize_url(link) for link in links))

            for link in links:
                get_url = requests.get(link)
                soup = BeautifulSoup(get_url.text, "html.parser")
                headline = soup.select('h1.ArticleHeader-headline')
                if len(headline) > 0:
                    headline = headline[0].get_text()
                    link_list.append(link)
                    headline_list.append(headline)
                    zipped_list = zip(link_list, headline_list)
            return zipped_list

        news = get_news()
        st.subheader("News")
        for link, headline in news:
            styled_link = f'<a href="{link}" style="font-size: 25px;">{headline}</a>'
            st.markdown(styled_link, unsafe_allow_html=True)
            st.write("")

    with tab2:
        st.subheader('Realtime Stock Monitoring')
        ticker = st.selectbox('Select a stock ticker', ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS', 'BABA', 'WMT', 'PG'])
        # Fetch real-time stock data
        @st.cache_data
        def get_data(ticker):
            data = yf.download(ticker, period="1y", interval="1d")
            return data

        # Display the stock data
        def display_data():
            data = get_data(ticker)
            st.write(f"Daily Close Price of {ticker} [Last 365 Days]")
            st.line_chart(data['Close'])

        if ticker:
            display_data()
            #pass
        with tab3:
            pass
        with tab4:
            pass
        with tab5:
            pass

else:
    st.warning("Please log in to access Finance Adviser.")