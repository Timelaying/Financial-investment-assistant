# Importing necessary libraries
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

        data2 = yf.download(ticker, period="max")

        # Feature Engineering
        data2["Tomorrow"] = data2["Close"].shift(-1)  # Create a column for tomorrow's closing price
        data2["Target"] = (data2["Tomorrow"] > data2["Close"]).astype(int)  # Create target variable (1 if price increases, 0 otherwise)
        data2 = data2.loc["1990-01-01":].copy()  # Filter data from 1990 onwards

        # Training the model
        model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
        predictors = ["Open", "Close", "High", "Low", "Volume"]  # Features for prediction

        # Function to predict and evaluate
        def predict_and_evaluate(train, test, predictors, model):
            model.fit(train[predictors], train["Target"])
            preds = model.predict(test[predictors])
            accuracy = accuracy_score(test["Target"], preds)
            precision = precision_score(test["Target"], preds)
            return preds, accuracy, precision

        # Backtesting with rolling windows
        def backtest(data, model, predictors, start=2500, step=250):
            all_predictions = []
            accuracies = []
            precisions = []
            for i in range(start, data.shape[0], step):
                train = data.iloc[0:i].copy()
                test = data.iloc[i:(i + step)].copy()
                predictions, accuracy, precision = predict_and_evaluate(train, test, predictors, model)
                all_predictions.append(pd.Series(predictions, index=test.index, name="Predictions"))
                accuracies.append(accuracy)
                precisions.append(precision)
            return pd.concat(all_predictions), np.mean(accuracies), np.mean(precisions)

        # Perform backtesting
        predictions, accuracy, precision = backtest(data2, model, predictors)

        # Display model evaluation metrics
        st.subheader("Model Evaluation Metrics")
        st.write(f"Accuracy: {accuracy:.2f}")
        st.write(f"Precision: {precision:.2f}")

        # Feature Importance
        st.subheader("Feature Importance")
        model.fit(data2[predictors], data2["Target"])  # Refit the model on entire data
        feature_importance = pd.DataFrame({'Feature': predictors, 'Importance': model.feature_importances_})
        feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
        st.bar_chart(feature_importance.set_index('Feature'))

        # Investment Recommendation
        st.subheader("Investment Recommendation")
        last_day_data = data2.iloc[-1]
        last_day_close = last_day_data["Close"]
        last_day_features = last_day_data[predictors].values.reshape(1, -1)
        next_day_prediction = model.predict(last_day_features)[0]
        prediction_confidence = model.predict_proba(last_day_features)[0][next_day_prediction]
        prediction_label = "High" if next_day_prediction == 1 else "Low"
        advice = "Invest" if next_day_prediction == 1 else "Do Not Invest"
        st.write(f"Predicted Closing Price for Next Day: {prediction_label}")
        st.write(f"Confidence: {prediction_confidence:.2f}")
        st.write(f"Advice: {advice}")




    with tab3:
        class TradingSimulator:
            def __init__(self):
                self.num_days = 100
                self.base_price = 100
                self.volatility = 0.02
                self.strategy = 'simple'  # Default trading strategy
                self.data_source = 'simulated'  # Default data source

            def generate_price_data(self):
                """Generate simulated or historical price data."""
                if self.data_source == 'historical':
                    # Download historical data from Yahoo Finance
                    data = yf.download("AAPL", period="1y")
                    price_data = data['Close'].to_numpy()
                else:
                    # Simulate price data
                    trend = np.sin(np.linspace(0, 10, self.num_days)) * 10
                    noise = np.random.normal(0, self.volatility, self.num_days)
                    price_data = np.cumsum(trend + noise) + self.base_price
                return price_data

            def simulate_trades(self, price_data, initial_balance):
                """Simulate trades based on the selected trading strategy."""
                balance = initial_balance
                buy_signal = True

                for i in range(1, len(price_data)):
                    if price_data[i] > price_data[i - 1] and buy_signal:
                        shares = balance / price_data[i]
                        balance = 0
                        buy_signal = False
                    elif price_data[i] < price_data[i - 1] and not buy_signal:
                        balance = shares * price_data[i]
                        buy_signal = True

                return balance

            def candlestick_chart(self, price_data):
                """Generate a candlestick chart with price data."""
                fig = go.Figure()

                fig.add_trace(go.Scatter(x=np.arange(len(price_data)), y=price_data, mode='lines', name='Price'))
                fig.add_trace(go.Candlestick(x=np.arange(len(price_data)),
                                            open=price_data,
                                            high=price_data + 2 * np.random.rand(len(price_data)),
                                            low=price_data - 2 * np.random.rand(len(price_data)),
                                            close=price_data,
                                            name='Candlestick'))

                fig.update_layout(title='Simulated Market Data (Candlestick Chart)',
                                xaxis_title='Days',
                                yaxis_title='Price',
                                xaxis_rangeslider_visible=False)

                return fig


        def main():
            st.title('Trading Simulator')

            # Sidebar for simulator parameters
            st.sidebar.header('Parameters')
            num_days = st.sidebar.slider('Number of Days', min_value=10, max_value=1000, value=100)
            volatility = st.sidebar.slider('Volatility', min_value=0.01, max_value=0.10, value=0.02)
            initial_balance = st.sidebar.number_input("Initial Balance ($)", min_value=1, step=1, value=10000)
            strategy = st.sidebar.selectbox('Trading Strategy', ['simple', 'historical'])
            if strategy == 'historical':
                st.sidebar.warning("Using historical data from Yahoo Finance.")

            # Initialize TradingSimulator
            simulator = TradingSimulator()
            simulator.num_days = num_days
            simulator.volatility = volatility
            simulator.strategy = strategy

            # Simulate market
            price_data = simulator.generate_price_data()

            # Candlestick chart
            st.subheader('Candlestick Chart')
            candlestick_chart = simulator.candlestick_chart(price_data)
            st.plotly_chart(candlestick_chart)

            # Display balance
            final_balance = simulator.simulate_trades(price_data, initial_balance)
            st.write(f"Initial Balance: ${initial_balance:.2f}")
            st.write(f"Final Balance: ${final_balance:.2f}")


        if __name__ == "__main__":
            main()


            #pass
    with tab4:
        st.title("Reading Resources")

        st.write("""
        Welcome to the Reading Resources section! Here, you can find various educational materials to enhance your understanding of investment fundamentals and make informed decisions.
        """)

        st.subheader("Educational Articles")
        with st.expander("📚 Click to view articles"):
            st.markdown("""
            - [Introduction to Investing](https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp): Learn the basics of the stock market and how it operates.
            - [Understanding Stocks](https://www.nerdwallet.com/article/investing/what-are-stocks): Discover what stocks are and how they work as investment vehicles.
            - [Guide to Mutual Funds](https://www.sec.gov/reportspubs/investor-publications/investorpubsmfintrohtm.html): Get insights into mutual funds and how to invest in them.
            - [Basics of Bonds](https://www.investor.gov/introduction-investing/basics/investment-products/bonds-or-fixed-income-products): Understand the fundamentals of bonds and fixed-income products.
            - [ETFs vs. Mutual Funds](https://www.investor.gov/introduction-investing/basics/investment-products/mutual-funds-and-etfs): Learn about the differences between ETFs and mutual funds.
            - [Diversification: A Risk Management Strategy](https://www.sec.gov/reportspubs/investor-publications/investorpubsdiversificationhtm.html): Explore the concept of diversification as a risk management strategy.
            """)

        st.subheader("Video Tutorials")
        with st.expander("🎥 Click to watch tutorials"):
            st.markdown("""
            - [Investing for Beginners](https://www.youtube.com/watch?v=F3QpgXBtDeo): Beginner-friendly tutorial on investing principles.
            - [How to Choose Stocks](https://www.youtube.com/watch?v=fi7Km2zFfLk): Guidance on selecting stocks for investment.
            - [Understanding Mutual Funds](https://www.youtube.com/watch?v=2JCYn4CUEQ4): Video explaining mutual funds and their benefits.
            - [Introduction to Bonds](https://www.youtube.com/watch?v=iTAK3Rt1R1k): Introduction to bonds and bond investing.
            - [Value Investing Principles](https://www.youtube.com/watch?v=crI4KRqYttM): Learn about value investing strategies.
            - [Risk Management Strategies](https://www.youtube.com/watch?v=K6fCnXJ2F24): Explore different risk management techniques for investments.
            """)

        st.subheader("Podcasts")
        with st.expander("🎧 Click to listen to podcasts"):
            st.markdown("""
            - [InvestED Podcast](https://www.ruleoneinvesting.com/podcast/): Dive deep into investing with insights from experienced investors.
            - [The Investor's Podcast Network](https://www.theinvestorspodcast.com/): Network of podcasts covering various investment topics.
            - [The Motley Fool Podcasts](https://www.fool.com/podcasts/): Listen to discussions on finance and investing by Motley Fool experts.
            - [We Study Billionaires](https://www.theinvestorspodcast.com/): Podcast focused on billionaire investors and their strategies.
            - [Market Foolery](https://www.fool.com/podcasts/marketfoolery/): Stay updated on market news and analysis with this podcast.
            """)

        st.subheader("Recommended Books")
        with st.expander("📖 Click to view recommended books"):
            st.markdown("""
            - "The Intelligent Investor" by Benjamin Graham: Classic book on value investing principles.
            - "A Random Walk Down Wall Street" by Burton G. Malkiel: Insights into efficient market theory and investment strategies.
            - "The Little Book of Common Sense Investing" by John C. Bogle: Guide to passive investing and index funds.
            - "The Essays of Warren Buffett: Lessons for Corporate America" by Warren Buffett: Learn from the legendary investor's wisdom.
            - "Common Stocks and Uncommon Profits" by Philip Fisher: Detailed analysis of stock selection and investment strategies.
            - "One Up On Wall Street" by Peter Lynch: Insights from one of the most successful investors of all time.
            """)

        st.subheader("Online Courses")
        with st.expander("🎓 Click to enroll in courses"):
            st.markdown("""
            - [Coursera - Financial Markets](https://www.coursera.org/learn/financial-markets-global): Learn about global financial markets and investment strategies.
            - [Udemy - Investment Management](https://www.udemy.com/course/investment-management/): Comprehensive course covering various aspects of investment management.
            - [edX - Finance Essentials](https://www.edx.org/learn/finance-essentials): Essential finance concepts and principles taught by industry experts.
            - [Khan Academy - Investment and Retirement](https://www.khanacademy.org/college-careers-more/personal-finance): Free courses on investment and retirement planning.
            - [LinkedIn Learning - Investment Strategies](https://www.linkedin.com/learning/investment-strategies/): Develop investment strategies and portfolio management skills.
            """)
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
                            df['Middle Band'] = ta.volatility.bollinger_mavg(df.Close)
                            df['Upper Band'], df['Lower Band'] = ta.volatility.bollinger_hband(df.Close), ta.volatility.bollinger_lband(df.Close)

                            # Determine overbought and oversold conditions
                            df.loc[(df.Close > df['Upper Band']), 'Bollinger Bands'] = 'Overbought'
                            df.loc[(df.Close < df['Lower Band']), 'Bollinger Bands'] = 'Oversold'

                            if investment_style == "Value Investing":
                                buy_condition = df.Close < df['Lower Band']
                                sell_condition = df.Close > df['Upper Band']
                            elif investment_style == "Growth Investing":
                                buy_condition = df.Close > df['Upper Band']
                                sell_condition = df.Close < df['Lower Band']
                            else:
                                buy_condition = False
                                sell_condition = False

                            # Apply buy, sell, and hold labels based on investment style
                            df.loc[buy_condition, 'Bollinger Bands'] = 'Buy'
                            df.loc[sell_condition, 'Bollinger Bands'] = 'Sell'
                            df.loc[~(buy_condition | sell_condition), 'Bollinger Bands'] = 'Hold'

                            # Add another column to explicitly indicate overbought or oversold
                            df['Overbought/Oversold'] = ''
                            df.loc[(df.Close > df['Upper Band']), 'Overbought/Oversold'] = 'Overbought'
                            df.loc[(df.Close < df['Lower Band']), 'Overbought/Oversold'] = 'Oversold'


                        # Volume Analysis recommendation with risk tolerance context
                        def Volume_Analysis(df, risk_tolerance):
                            df['Volume SMA50'] = df['Volume'].rolling(window=50).mean()
                            df['Volume SMA200'] = df['Volume'].rolling(window=200).mean()
                            df.loc[df['Volume SMA50'] > df['Volume SMA200'], 'Volume Analysis'] = 'Increasing Volume'
                            df.loc[df['Volume SMA50'] < df['Volume SMA200'], 'Volume Analysis'] = 'Decreasing Volume'
                            df.loc[~((df['Volume SMA50'] > df['Volume SMA200']) | (df['Volume SMA50'] < df['Volume SMA200'])), 'Volume Analysis'] = 'Stable Volume'


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

                            # Add another column to explicitly indicate increasing or decreasing volume
                            df['Increasing/Decreasing Volume'] = ''
                            df.loc[df['Volume SMA50'] > df['Volume SMA200'], 'Increasing/Decreasing Volume'] = 'Increasing Volume'
                            df.loc[df['Volume SMA50'] < df['Volume SMA200'], 'Increasing/Decreasing Volume'] = 'Decreasing Volume'
                            df.loc[~((df['Volume SMA50'] > df['Volume SMA200']) | (df['Volume SMA50'] < df['Volume SMA200'])), 'Increasing/Decreasing Volume'] = 'Stable Volume'

                            # For demonstration purposes, let's assume simple moving averages on volume data
                            df['Volume SMA20'] = df['Volume'].rolling(window=20).mean()
                            df['Volume SMA50'] = df['Volume'].rolling(window=50).mean()
                            df['Volume Support'] = df['Volume SMA20'] * 0.95  # Support level at 95% of SMA20
                            df['Volume Resistance'] = df['Volume SMA50'] * 1.05  # Resistance level at 105% of SMA50



                        # On-Balance Volume recommendation with investment horizon context
                        def On_Balance_Volume(df, investment_horizon):
                            if not df.empty:
                                df['OBV'] = ta.volume.on_balance_volume(df.Close, df.Volume)
                                df['OBV Change'] = df['OBV'].diff()
                                df['OBV'] = df['OBV'].astype('object')

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

                                # Add another column to explicitly indicate OBV change
                                df['OBV Change Direction'] = ''
                                df.loc[df['OBV Change'] > 0, 'OBV Change Direction'] = 'Bullish'
                                df.loc[df['OBV Change'] < 0, 'OBV Change Direction'] = 'Bearish'

                        # Support and Resistance Levels recommendation with investment horizon context
                        def Support_Resistance_Levels(df, investment_horizon):
                            df['Support Level'] = df['Low'].rolling(window=20).min()
                            df['Resistance Level'] = df['High'].rolling(window=20).max()
                            
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

                            #Extra Complexity for support
                             # For demonstration purposes, let's assume simple moving averages on price data
                            df['SMA20'] = df['Close'].rolling(window=20).mean()
                            df['SMA50'] = df['Close'].rolling(window=50).mean()
                            df['Support'] = df['SMA20'] * 0.95  # Support level at 95% of SMA20
                            df['Resistance'] = df['SMA50'] * 1.05  # Resistance level at 105% of SMA50

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

                        # Display the results DataFrame
                        st.subheader("Results")
                        st.write('1. Full details')
                        st.write(df)
                        st.write('2. Summary')
                        summarized_results = df[['Decision MACD', 'Decision RSI/SMA', 'Bollinger Bands', 'Volume Analysis',
                                                        'OBV', 'Support Resistance']]
                        st.write(summarized_results)

                    except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

                    
                    
                            
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
        # Define Portfolio class
        class Portfolio:
            def __init__(self):
                self.weights = None
                self.transactions = pd.DataFrame(columns=["Date", "Type", "Asset", "Quantity", "Price"])
            
            def add_transaction(self, date, transaction_type, asset, quantity, price):
                self.transactions = self.transactions.append({
                    "Date": date,
                    "Type": transaction_type,
                    "Asset": asset,
                    "Quantity": quantity,
                    "Price": price
                }, ignore_index=True)
            
            def clear_transaction_history(self):
                self.transactions = pd.DataFrame(columns=["Date", "Type", "Asset", "Quantity", "Price"])
            
            def portfolio_value(self):
                return (self.transactions["Quantity"] * self.transactions["Price"]).sum()
            
            def calculate_weights(self):
                returns = expected_returns.mean_historical_return(self.transactions)
                cov_matrix = risk_models.sample_cov(self.transactions)
                ef = EfficientFrontier(returns, cov_matrix)
                self.weights = ef.max_sharpe_ratio()
            
            def plot_portfolio_performance(self):
                # Placeholder for portfolio performance chart
                # Add your code to plot the portfolio performance using self.weights
                pass
            
            def transaction_history(self):
                return self.transactions
            
            def export_data(self, format="csv"):
                if format == "csv":
                    self.transactions.to_csv("portfolio_transactions.csv", index=False)
                elif format == "excel":
                    self.transactions.to_excel("portfolio_transactions.xlsx", index=False)

        # Streamlit app
        st.title("Portfolio Management")

        # Instantiate Portfolio object
        if 'portfolio' not in st.session_state:
            st.session_state.portfolio = Portfolio()

        # Add transaction to the portfolio
        st.subheader("Add Transaction")
        date = st.date_input("Date", value=datetime.today())
        transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
        asset = st.text_input("Asset")
        quantity = st.number_input("Quantity", min_value=0)
        price = st.number_input("Price", min_value=0.01)
        if st.button("Add Transaction"):
            st.session_state.portfolio.add_transaction(date, transaction_type, asset, quantity, price)
            st.success("Transaction added successfully.")

        # View portfolio value and performance
        st.subheader("Portfolio Overview")
        portfolio_value = st.session_state.portfolio.portfolio_value()
        st.write(f"Portfolio Value: ${portfolio_value:.2f}")

        # Calculate and display portfolio weights
        if st.button("Calculate Weights"):
            st.session_state.portfolio.calculate_weights()
            st.write("Portfolio Weights:")
            st.write(st.session_state.portfolio.weights)

        # Plot portfolio performance
        st.subheader("Portfolio Performance Chart")
        performance_chart = st.session_state.portfolio.plot_portfolio_performance()
        st.plotly_chart(performance_chart)

        # View transaction history
        st.subheader("Transaction History")
        transaction_history = st.session_state.portfolio.transaction_history()
        st.write(transaction_history)



else:
    st.warning("Please log in to access Finance Adviser.")