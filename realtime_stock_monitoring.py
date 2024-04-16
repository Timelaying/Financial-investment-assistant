import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

def display_data(ticker):
    data = get_data(ticker)
    st.write(f"Daily Close Price of {ticker} [Last 365 Days]")
    st.line_chart(data['Close'])

@st.cache_data
def get_data(ticker):
    data = yf.download(ticker, period="1y", interval="1d")
    return data

def predict_and_evaluate(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    accuracy = accuracy_score(test["Target"], preds)
    precision = precision_score(test["Target"], preds)
    return preds, accuracy, precision

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

def render_realtime_stock_monitoring():
    st.subheader('Realtime Stock Monitoring')
    ticker = st.selectbox('Select a stock ticker',
                        ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'JPM', 'V', 'NVDA', 'NFLX', 'DIS',
                        'BABA', 'WMT', 'PG'])

    if ticker:
        display_data(ticker)

    generate_prediction = st.button("Generate Prediction and Analysis")

    if generate_prediction:
        with st.spinner("Fetching and processing data..."):

            data2 = yf.download(ticker, period="max")
            data2["Tomorrow"] = data2["Close"].shift(-1)
            data2["Target"] = (data2["Tomorrow"] > data2["Close"]).astype(int)
            data2 = data2.loc["1990-01-01":].copy()

            model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
            predictors = ["Open", "Close", "High", "Low", "Volume"]

            predictions, accuracy, precision = backtest(data2, model, predictors)

            st.subheader("Model Evaluation Metrics")
            st.write(f"Accuracy: {accuracy:.2f}")
            st.write(f"Precision: {precision:.2f}")

            model.fit(data2[predictors], data2["Target"])
            feature_importance = pd.DataFrame({'Feature': predictors, 'Importance': model.feature_importances_})
            feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
            st.subheader("Feature Importance")
            st.bar_chart(feature_importance.set_index('Feature'))

            last_day_data = data2.iloc[-1]
            last_day_features = last_day_data[predictors].values.reshape(1, -1)
            next_day_prediction = model.predict(last_day_features)[0]
            prediction_confidence = model.predict_proba(last_day_features)[0][next_day_prediction]
            prediction_label = "High" if next_day_prediction == 1 else "Low"
            advice = "Invest" if next_day_prediction == 1 else "Do Not Invest"
            st.subheader("Investment Recommendation")
            st.write(f"Predicted Closing Price for Next Day: {prediction_label}")
            st.write(f"Confidence: {prediction_confidence:.2f}")
            st.write(f"Advice: {advice}")
