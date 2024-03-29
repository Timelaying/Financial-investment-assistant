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
    # Create a placeholder for the form

    form_placeholder = st.empty()

    # Use the placeholder to display the form
    with form_placeholder.form("Question"):
         # Introduction
        st.write(
        """
        Welcome to the Portfolio Goals page! Here, you can define your investment objectives and preferences.
        Please fill out the following fields to help us tailor investment recommendations for you.
        """)

        # Goal
        st.subheader("Goal")        
        goal = st.text_input("What is your investmentent goal?", value="", type="default")

        # stocks of interest
        st.subheader("Stocks of interest")
        option = st.multiselect(
            'What stocks are you interested in?',
            ('Google', 'Apple', 'Nvidia'))
        
        st.subheader("Risk Tolerance")
        risk_tolerance = st.selectbox(
        "Select your risk tolerance",
        ["Low - I prefer stability over potential returns",
        "Medium - I'm comfortable with moderate fluctuations",
        "High - I'm willing to take high risks for potential high returns"])

        # Investment horizon
        st.subheader("Investment Horizon")
        investment_horizon = st.selectbox(
            "Select your investment horizon",
            ["Short-term - 1 to 3 years",
            "Medium-term - 3 to 5 years",
            "Long-term - 5 years or more"])
        
        # Investment amount
        st.subheader("Investment Amount")
        investment_amount = st.number_input(
            "Enter your investment amount ($)",
            min_value=0.0,
            step=100.0,
            value=1000.0)       

        # Types of stocks
        st.subheader("Types of Stocks")
        types_of_stocks = st.multiselect(
            "Select types of stocks you're interested in",
            ["Technology", "Finance", "Healthcare", "Consumer Goods"]) 

        # Investment style
        st.subheader("Investment Style")
        investment_style = st.radio(
            "Select your investment style",
            ["Value Investing", "Growth Investing", "Index Investing"])                
        
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Clear the placeholder to hide the form
        form_placeholder.empty()

        # Display the tabs after form submission
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

                 # # Function to fetch news from NewsAPI
            # def get_financial_news(api_key='1ced749db7134f5684df1227101cd72f', language='en', category='business'):
            #     base_url = "https://newsapi.org/v2/top-headlines"
            #     params = {
            #         'language': language,
            #         'category': category,
            #         'apiKey': api_key
            #     }
            #     response = requests.get(base_url, params=params)
            #     news_data = response.json()
            #     return news_data['articles']
            
            # # Fetch news on page load
            # articles = get_financial_news()

            # for article in articles:
            #     st.subheader(article['title'])
            #     st.write(article['description'])
            #     st.markdown(f"[Read More]({article['url']})", unsafe_allow_html=True)

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