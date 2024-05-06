import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score

@st.cache
def get_data(ticker, period="1y"):
    data = yf.download(ticker, period=period, interval="1d")
    return data

def compute_target_column(data):
    data["Tomorrow"] = data["Close"].shift(-1)
    data["Target"] = (data["Tomorrow"] > data["Close"]).astype(int)
    data.dropna(inplace=True)  # Remove rows with NaN values
    return data

def train_models():
    rf_model = RandomForestClassifier(n_estimators=100, min_samples_split=50, random_state=1)
    xgb_model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=1)
    svm_model = SVC(kernel='rbf', C=1, gamma='scale', probability=True, random_state=1)
    return [("rf", rf_model), ("xgb", xgb_model), ("svm", svm_model)]

@st.cache
def backtest(data, models):
    data = compute_target_column(data)
    predictors = ["Open", "Close", "High", "Low", "Volume"]
    train_size = int(0.8 * len(data))
    train = data.iloc[:train_size]
    test = data.iloc[train_size:]
    for _, model in models:
        model.fit(train[predictors], train["Target"])
    preds = [model.predict(test[predictors]) for _, model in models]
    preds = np.mean(preds, axis=0) > 0.5  # Take the average prediction and convert to binary
    accuracy = accuracy_score(test["Target"], preds)
    precision = precision_score(test["Target"], preds, zero_division=1)  # Addressing warning
    return preds, accuracy, precision

def display_data(data):
    st.write(f"Daily Close Price [Last {len(data)} Days]")
    st.line_chart(data['Close'])

def render_realtime_stock_monitoring():
    st.subheader('Realtime Stock Monitoring')
    ticker = st.selectbox('Select a stock ticker',
                          ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                           'BABA', 'WMT', 'PG'])

    if ticker:
        period = st.radio("Select the period", ["1y", "2y", "5y"])  # Limiting historical data to reduce load time
        data = get_data(ticker, period=period)
        display_data(data)

        generate_prediction = st.button("Generate Prediction and Analysis")

        if generate_prediction:
            with st.spinner("Fetching and processing data..."):
                models = train_models()
                preds, accuracy, precision = backtest(data, models)
                st.subheader("Model Evaluation Metrics")
                st.write(f"Accuracy: {accuracy:.2f}")
                st.write(f"Precision: {precision:.2f}")
                st.subheader("Investment Recommendation")
                st.write("Predicted Closing Price for Next Day: ", "High" if preds[-1] == 1 else "Low")
                st.write("Confidence: ", np.mean(preds))
                st.write("Advice: ", "Invest" if preds[-1] == 1 else "Do Not Invest")

