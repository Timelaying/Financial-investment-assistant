import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import pandas_ta

# Function to make MACD-based decisions
def MACDdecision(df, risk_tolerance):
    # Determine the threshold based on risk tolerance
    if risk_tolerance == "High":
        threshold = 0.2
    elif risk_tolerance == "Medium":
        threshold = 0.1
    else:
        threshold = 0

    # Calculate MACD difference and make decisions
    df['MACD_diff'] = ta.trend.macd_diff(df.Close)
    df.loc[(df.MACD_diff > threshold) & (df.MACD_diff.shift(1) < threshold), 'Decision MACD'] = 'Buy'
    df.loc[~(df.MACD_diff > threshold) & (df.MACD_diff.shift(1) < threshold), 'Decision MACD'] = "Don't Buy"

# Function to make RSI and SMA-based decisions
def RSI_SMAdecision(df, investment_horizon):
    # Determine RSI threshold based on investment horizon
    if investment_horizon == "Short-term - 1 to 3 years":
        RSI_threshold = 30
    elif investment_horizon == "Medium-term - 3 to 5 years":
        RSI_threshold = 40
    elif investment_horizon == "Long-term - 5 years or more":
        RSI_threshold = 50
    else:
        RSI_threshold = 0

    # Calculate RSI and SMA and make decisions
    df['RSI'] = ta.momentum.rsi(df.Close, window=10)
    df['SMA200'] = ta.trend.sma_indicator(df.Close, window=200)
    df.loc[(df.Close > df.SMA200) & (df.RSI < RSI_threshold), 'Decision RSI/SMA'] = 'Buy'
    df.loc[~((df.Close > df.SMA200) & (df.RSI < RSI_threshold)), 'Decision RSI/SMA'] = "Don't Buy"

# Function to analyze Bollinger Bands
def Bollinger_Bands(df, investment_style):
    # Calculate Bollinger Bands
    df['Middle Band'] = ta.volatility.bollinger_mavg(df.Close)
    df['Upper Band'], df['Lower Band'] = ta.volatility.bollinger_hband(df.Close), ta.volatility.bollinger_lband(df.Close)

    # Determine buy, sell, or hold conditions based on investment style
    if investment_style == "Value Investing":
        buy_condition = df.Close < df['Lower Band']
        sell_condition = df.Close > df['Upper Band']
    elif investment_style == "Growth Investing":
        buy_condition = df.Close > df['Upper Band']
        sell_condition = df.Close < df['Lower Band']
    else:
        buy_condition = False
        sell_condition = False

    # Assign buy, sell, hold labels
    df.loc[buy_condition, 'Bollinger Bands'] = 'Buy'
    df.loc[sell_condition, 'Bollinger Bands'] = 'Sell'
    df.loc[~(buy_condition | sell_condition), 'Bollinger Bands'] = 'Hold'

    # Additional analysis for overbought/oversold
    df['Overbought/Oversold'] = ''
    df.loc[(df.Close > df['Upper Band']), 'Overbought/Oversold'] = 'Overbought'
    df.loc[(df.Close < df['Lower Band']), 'Overbought/Oversold'] = 'Oversold'

# Function to analyze volume data
def Volume_Analysis(df, risk_tolerance):
    # Calculate rolling averages for volume
    df['Volume SMA50'] = df['Volume'].rolling(window=50).mean()
    df['Volume SMA200'] = df['Volume'].rolling(window=200).mean()

    # Determine buy, sell, hold conditions based on volume and risk tolerance
    if risk_tolerance == "High":
        volume_threshold = 0.3
    elif risk_tolerance == "Medium":
        volume_threshold = 0.2
    else:
        volume_threshold = 0.1

    # Assign buy, sell, hold labels
    df.loc[df['Volume SMA50'] > df['Volume SMA200'], 'Volume Analysis'] = 'Increasing Volume'
    df.loc[df['Volume SMA50'] < df['Volume SMA200'], 'Volume Analysis'] = 'Decreasing Volume'
    df.loc[~((df['Volume SMA50'] > df['Volume SMA200']) | (df['Volume SMA50'] < df['Volume SMA200'])), 'Volume Analysis'] = 'Stable Volume'

    df.loc[df['Volume SMA50'] > df['Volume SMA200'] * (1 + volume_threshold), 'Volume Analysis'] = 'Buy'
    df.loc[df['Volume SMA50'] < df['Volume SMA200'] * (1 - volume_threshold), 'Volume Analysis'] = 'Sell'
    df.loc[~((df['Volume SMA50'] > df['Volume SMA200'] * (1 + volume_threshold)) |
              (df['Volume SMA50'] < df['Volume SMA200'] * (1 - volume_threshold))), 'Volume Analysis'] = 'Hold'

    df['Increasing/Decreasing Volume'] = ''
    df.loc[df['Volume SMA50'] > df['Volume SMA200'], 'Increasing/Decreasing Volume'] = 'Increasing Volume'
    df.loc[df['Volume SMA50'] < df['Volume SMA200'], 'Increasing/Decreasing Volume'] = 'Decreasing Volume'
    df.loc[~((df['Volume SMA50'] > df['Volume SMA200']) | (df['Volume SMA50'] < df['Volume SMA200'])), 'Increasing/Decreasing Volume'] = 'Stable Volume'

    df['Volume SMA20'] = df['Volume'].rolling(window=20).mean()
    df['Volume SMA50'] = df['Volume'].rolling(window=50).mean()
    df['Volume Support'] = df['Volume SMA20'] * 0.95
    df['Volume Resistance'] = df['Volume SMA50'] * 1.05

# Function to analyze On-Balance Volume (OBV)
def On_Balance_Volume(df, investment_horizon):
    # Calculate OBV and OBV change
    df['OBV'] = ta.volume.on_balance_volume(df.Close, df.Volume)
    df['OBV Change'] = df['OBV'].diff()
    df['OBV'] = df['OBV'].astype('object')

    # Determine buy, sell, hold conditions based on OBV change direction and investment horizon
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

    # Assign buy, sell, hold labels
    df.loc[buy_condition, 'OBV'] = 'Buy'
    df.loc[sell_condition, 'OBV'] = 'Sell'
    df.loc[~(buy_condition | sell_condition), 'OBV'] = 'Hold'

    df['OBV Change Direction'] = ''
    df.loc[df['OBV Change'] > 0, 'OBV Change Direction'] = 'Bullish'
    df.loc[df['OBV Change'] < 0, 'OBV Change Direction'] = 'Bearish'

# Function to analyze Support and Resistance Levels
def Support_Resistance_Levels(df, investment_horizon):
    # Calculate support and resistance levels
    df['Support Level'] = df['Low'].rolling(window=20).min()
    df['Resistance Level'] = df['High'].rolling(window=20).max()

    # Determine buy, sell, hold conditions based on investment horizon
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

    # Assign buy, sell, hold labels
    df.loc[buy_condition, 'Support Resistance'] = 'Buy'
    df.loc[sell_condition, 'Support Resistance'] = 'Sell'
    df.loc[~(buy_condition | sell_condition), 'Support Resistance'] = 'Hold'

    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['Support'] = df['SMA20'] * 0.95
    df['Resistance'] = df['SMA50'] * 1.05

# Function to generate recommendation results
def generate_recommendation_results():
    # Display user input options
    st.subheader("Recommendation Results")
    df = pd.DataFrame()
    ticker2 = st.selectbox('Select a stock ticker',
                           ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                            'BABA', 'WMT', 'PG'], key='t2')
    period = st.selectbox('Select the period for stock data', ['1mo', '3mo', '6mo', '1y'], key='p')
    interval = st.selectbox('Select the interval for stock data', ['1h', '1d'], key='i')

    change_preferences = st.radio("Do you want to change your preferences?", ('Yes', 'No'), key='cp')

    if change_preferences == 'Yes':
        risk_tolerance = st.selectbox('Select your risk tolerance', ['High', 'Medium', 'Low'], key='rt')
        investment_horizon = st.selectbox('Select your investment horizon', ['Short-term - 1 to 3 years', 'Medium-term - 3 to 5 years', 'Long-term - 5 years or more'], key='ih')
        investment_style = st.selectbox('Select your investment style', ['Value Investing', 'Growth Investing', 'Other'], key='is')
    else:
        # Use default values or previously selected values
        risk_tolerance = st.session_state.form_data['risk_tolerance']
        investment_horizon = st.session_state.form_data['investment_horizon']
        investment_style = st.session_state.form_data['investment_style']

    if st.button("Generate Recommendations"):
        with st.spinner("Fetching and processing data..."):
            try:
                df = df.ta.ticker(ticker2, period=period, interval=interval)

                generate_recommendations(df, risk_tolerance, investment_horizon, investment_style)

                st.success("Recommendations generated successfully!")

                st.subheader("Results")
                st.write('1. Full details')
                st.write(df)
                st.write('2. Summary')
                summarized_results = df[['Decision MACD', 'Decision RSI/SMA', 'Bollinger Bands', 'Volume Analysis',
                                         'OBV', 'Support Resistance']]
                st.write(summarized_results)

                recommendation_counts = df[['Decision MACD', 'Decision RSI/SMA', 'Bollinger Bands', 'Volume Analysis', 'OBV', 'Support Resistance']].apply(pd.Series.value_counts)

                plt.figure(figsize=(10, 6))
                recommendation_counts.plot(kind='bar', stacked=True)
                plt.title('Recommendation Counts by Indicator')
                plt.xlabel('Recommendation Type')
                plt.ylabel('Count')
                plt.xticks(rotation=45)
                plt.legend(title='Indicator')
                plt.tight_layout()
                st.pyplot(plt)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Function to generate recommendations based on technical indicators
def generate_recommendations(df, risk_tolerance, investment_horizon, investment_style):
    MACDdecision(df, risk_tolerance)
    RSI_SMAdecision(df, investment_horizon)
    Bollinger_Bands(df, investment_style)
    Volume_Analysis(df, risk_tolerance)
    On_Balance_Volume(df, investment_horizon)
    Support_Resistance_Levels(df, investment_horizon)

# Entry point of the Streamlit app
if __name__ == "__main__":
    generate_recommendation_results()
