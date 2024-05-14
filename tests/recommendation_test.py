import pytest  # Importing pytest for testing
import pandas as pd  # Importing pandas for data manipulation
import sys  # Importing sys for system-specific parameters and functions
import os  # Importing os for operating system dependent functionality

# Add parent directory to sys.path to ensure modules in the parent directory can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import custom module 'recommendation_results' from the parent directory
from recommendation_results import *

# Define a pytest fixture for a sample DataFrame
@pytest.fixture
def sample_dataframe():
    # Creating a sample DataFrame with some columns and data
    return pd.DataFrame({
        'Close': [100, 105, 110, 115, 120],
        'Volume': [100000, 110000, 120000, 130000, 140000],
        'Low': [90, 95, 100, 105, 110],  # Adding a 'Low' column with some sample data
        'High': [90, 95, 100, 105, 110]  # Adding a 'High' column with some sample data
    })

# Test the MACD decision function
def test_MACD_decision(sample_dataframe):
    risk_tolerance = "High"
    MACDdecision(sample_dataframe, risk_tolerance)
    assert 'Decision MACD' in sample_dataframe.columns

# Test the RSI/SMA decision function
def test_RSI_SMA_decision(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    RSI_SMAdecision(sample_dataframe, investment_horizon)
    assert 'Decision RSI/SMA' in sample_dataframe.columns

# Test the Bollinger Bands function
def test_Bollinger_Bands(sample_dataframe):
    investment_style = "Value Investing"
    Bollinger_Bands(sample_dataframe, investment_style)
    assert 'Bollinger Bands' in sample_dataframe.columns

# Test the Volume Analysis function
def test_Volume_Analysis(sample_dataframe):
    risk_tolerance = "High"
    Volume_Analysis(sample_dataframe, risk_tolerance)
    assert 'Volume Analysis' in sample_dataframe.columns

# Test the On Balance Volume function
def test_On_Balance_Volume(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    On_Balance_Volume(sample_dataframe, investment_horizon)
    assert 'OBV' in sample_dataframe.columns

# Test the Support and Resistance Levels function
def test_Support_Resistance_Levels(sample_dataframe):
    investment_horizon = "Short-term - 1 to 3 years"
    Support_Resistance_Levels(sample_dataframe, investment_horizon)
    assert 'Support Resistance' in sample_dataframe.columns
