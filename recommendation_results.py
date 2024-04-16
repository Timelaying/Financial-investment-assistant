import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import pandas_ta

def generate_recommendation_results():
    st.subheader("Recommendation Results")

    df = pd.DataFrame()
    ticker2 = st.selectbox('Select a stock ticker',
                           ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                            'BABA', 'WMT', 'PG'], key='t2')
    period = st.selectbox('Select the period for stock data', ['1mo', '3mo', '6mo', '1y'], key='p')
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

                    # Extra Complexity for support
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

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
