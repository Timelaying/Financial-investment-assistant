import pytest
import pandas as pd
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import utils
from recommendation_results import *


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Close': [100, 105, 110, 115, 120],
        'Volume': [100000, 110000, 120000, 130000, 140000],
        'Low': [90, 95, 100, 105, 110],  # Adding a 'Low' column with some sample data
        'High': [90, 95, 100, 105, 110] # Adding a 'High
    })

def test_MACD_decision(sample_dataframe):
    risk_tolerance = "High"
    MACDdecision(sample_dataframe, risk_tolerance)
    assert 'Decision MACD' in sample_dataframe.columns

def test_RSI_SMA_decision(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    RSI_SMAdecision(sample_dataframe, investment_horizon)
    assert 'Decision RSI/SMA' in sample_dataframe.columns

def test_Bollinger_Bands(sample_dataframe):
    investment_style = "Value Investing"
    Bollinger_Bands(sample_dataframe, investment_style)
    assert 'Bollinger Bands' in sample_dataframe.columns

def test_Volume_Analysis(sample_dataframe):
    risk_tolerance = "High"
    Volume_Analysis(sample_dataframe, risk_tolerance)
    assert 'Volume Analysis' in sample_dataframe.columns

def test_On_Balance_Volume(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    On_Balance_Volume(sample_dataframe, investment_horizon)
    assert 'OBV' in sample_dataframe.columns

def test_Support_Resistance_Levels(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    Support_Resistance_Levels(sample_dataframe, investment_horizon)
    assert 'Support Resistance' in sample_dataframe.columns
