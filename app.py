# Importing necessary libraries
import requests
import pandas_ta
import ta
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from streamlit_login_auth_ui.widgets import __login__

# Set page configuration and header
st.set_page_config(page_title="Finance Adviser")
st.header("Finance Adviser")

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
        ticker = st.selectbox('Select a stock ticker',
                              ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                               'BABA', 'WMT', 'PG'])
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
            # pass
        with tab3:
            pass
        with tab4:
            pass
        with tab5:
            st.subheader("Recommendation Results")

            df = pd.DataFrame()
            ticker2 = st.selectbox('Select a stock ticker',
                                ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                                    'BABA', 'WMT', 'PG'], key = 't2')
            period = st.selectbox('Select the period for stock data', ['1mo', '3mo', '6mo', '1y'], key = 'p')
            interval = st.selectbox('Select the interval for stock data', ['1h', '1d'], key='i')

            if st.button("Generate Recommendations"):
                with st.spinner("Fetching and processing data..."):
                    try:
                        df = df.ta.ticker(ticker2, period=period, interval=interval)

                        # Recommendation of Stock using MACD with risk tolerance context
                        def MACDdecision(df, risk_tolerance):
                            if risk_tolerance == "High":
                                threshold = 0.2
                            elif risk_tolerance == "Medium":
                                threshold = 0.1
                            else:
                                threshold = 0

                            df['MACD_diff'] = ta.trend.macd_diff(df.Close)
                            df.loc[(df.MACD_diff > threshold) & (df.MACD_diff.shift(1) < threshold), 'Decision MACD'] = 'Buy'
                            df.loc[~(df.MACD_diff > threshold) & (df.MACD_diff.shift(1) < threshold), 'Decision MACD'] = 'Don\'t Buy'

                        # Recommendation of Stock using RSI and SMA with investment horizon context
                        def RSI_SMAdecision(df, investment_horizon):
                            if investment_horizon == "Short-term - 1 to 3 years":
                                RSI_threshold = 30
                            elif investment_horizon == "Medium-term - 3 to 5 years":
                                RSI_threshold = 40
                            elif investment_horizon == "Long-term - 5 years or more":
                                RSI_threshold = 50
                            else:
                                RSI_threshold = 0

                            df['RSI'] = ta.momentum.rsi(df.Close, window=10)
                            df['SMA200'] = ta.trend.sma_indicator(df.Close, window=200)
                            df.loc[(df.Close > df.SMA200) & (df.RSI < RSI_threshold), 'Decision RSI/SMA'] = 'Buy'
                            df.loc[~((df.Close > df.SMA200) & (df.RSI < RSI_threshold)), 'Decision RSI/SMA'] = 'Don\'t Buy'

                        # Bollinger Bands recommendation with investment style context
                        def Bollinger_Bands(df, investment_style):
                            if investment_style == "Value Investing":
                                buy_condition = df.Close < df['Lower Band']
                                sell_condition = df.Close > df['Upper Band']
                            elif investment_style == "Growth Investing":
                                buy_condition = df.Close > df['Upper Band']
                                sell_condition = df.Close < df['Lower Band']
                            else:
                                buy_condition = False
                                sell_condition = False

                            df['Middle Band'] = ta.volatility.bollinger_mavg(df.Close)
                            df['Upper Band'], df['Lower Band'] = ta.volatility.bollinger_hband(df.Close), ta.volatility.bollinger_lband(df.Close)
                            df.loc[buy_condition, 'Bollinger Bands'] = 'Buy'
                            df.loc[sell_condition, 'Bollinger Bands'] = 'Sell'
                            df.loc[~(buy_condition | sell_condition), 'Bollinger Bands'] = 'Hold'

                        # Volume Analysis recommendation with risk tolerance context
                        def Volume_Analysis(df, risk_tolerance):
                            if risk_tolerance == "High":
                                volume_threshold = 0.3
                            elif risk_tolerance == "Medium":
                                volume_threshold = 0.2
                            else:
                                volume_threshold = 0.1

                            df['Volume SMA50'] = df['Volume'].rolling(window=50).mean()
                            df['Volume SMA200'] = df['Volume'].rolling(window=200).mean()
                            df.loc[df['Volume SMA50'] > df['Volume SMA200'] * (1 + volume_threshold), 'Volume Analysis'] = 'Buy'
                            df.loc[df['Volume SMA50'] < df['Volume SMA200'] * (1 - volume_threshold), 'Volume Analysis'] = 'Sell'
                            df.loc[~((df['Volume SMA50'] > df['Volume SMA200'] * (1 + volume_threshold)) |
                                    (df['Volume SMA50'] < df['Volume SMA200'] * (1 - volume_threshold))), 'Volume Analysis'] = 'Hold'

                        # On-Balance Volume recommendation with investment horizon context
                        def On_Balance_Volume(df, investment_horizon):
                            if investment_horizon == "Short-term - 1 to 3 years":
                                buy_condition = df['OBV Change'] > 0
                                sell_condition = df['OBV Change'] < 0
                            elif investment_horizon == "Medium-term - 3 to 5 years":
                                buy_condition = df['OBV Change'] > 0
                                sell_condition = df['OBV Change'] < 0
                            elif investment_horizon == "Long-term - 5 years or more":
                                buy_condition = df['OBV Change'] > 0
                                sell_condition = df['OBV Change'] < 0
                            else:
                                buy_condition = False
                                sell_condition = False

                            df.loc[buy_condition, 'OBV'] = 'Buy'
                            df.loc[sell_condition, 'OBV'] = 'Sell'
                            df.loc[~(buy_condition | sell_condition), 'OBV'] = 'Hold'

                        # Support and Resistance Levels recommendation with investment horizon context
                        def Support_Resistance_Levels(df, investment_horizon):
                            if investment_horizon == "Short-term - 1 to 3 years":
                                buy_condition = df.Close > df['Support Level']
                                sell_condition = df.Close < df['Resistance Level']
                            elif investment_horizon == "Medium-term - 3 to 5 years":
                                buy_condition = df.Close > df['Support Level']
                                sell_condition = df.Close < df['Resistance Level']
                            elif investment_horizon == "Long-term - 5 years or more":
                                buy_condition = df.Close > df['Support Level']
                                sell_condition = df.Close < df['Resistance Level']
                            else:
                                buy_condition = False
                                sell_condition = False

                            df.loc[buy_condition, 'Support Resistance'] = 'Buy'
                            df.loc[sell_condition, 'Support Resistance'] = 'Sell'
                            df.loc[~(buy_condition | sell_condition), 'Support Resistance'] = 'Hold'

                         # Function to generate recommendations
                        def generate_recommendations(df, risk_tolerance, investment_horizon, investment_style):
                            MACDdecision(df, risk_tolerance)
                            RSI_SMAdecision(df, investment_horizon)
                            Bollinger_Bands(df, investment_style)
                            Volume_Analysis(df, risk_tolerance)
                            On_Balance_Volume(df, investment_horizon)
                            Support_Resistance_Levels(df, investment_horizon)

                        # Call the recommendation function with parameters
                        generate_recommendations(df, st.session_state.form_data['risk_tolerance'],
                                                st.session_state.form_data['investment_horizon'],
                                                st.session_state.form_data['investment_style'])

                        st.success("Recommendations generated successfully!")
                    except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

                    # Display the results DataFrame
                    st.subheader("Results")
                    show_summary = st.checkbox("Show Summary")
                    if show_summary:
                        summarized_results = df[['Decision MACD', 'Decision RSI/SMA', 'Bollinger Bands', 'Volume Analysis',
                                                'OBV', 'Support Resistance']]
                        st.write(summarized_results)
                    else:
                        st.write(df)

                    # Compute recommendation counts
                    recommendation_counts = df[['Decision MACD', 'Decision RSI/SMA', 'Bollinger Bands', 'Volume Analysis', 'OBV', 'Support Resistance']].apply(pd.Series.value_counts)

                    # Plot recommendation counts
                    plt.figure(figsize=(10, 6))
                    recommendation_counts.plot(kind='bar', stacked=True)
                    plt.title('Recommendation Counts by Indicator')
                    plt.xlabel('Recommendation Type')
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.legend(title='Indicator')
                    plt.tight_layout()
                    st.pyplot(plt)


        with tab6:
            pass

else:
    st.warning("Please log in to access Finance Adviser.")