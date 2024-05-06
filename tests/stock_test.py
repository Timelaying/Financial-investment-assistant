import pytest
from _pytest.monkeypatch import MonkeyPatch
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score


import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import utils
from realtime_stock_monitoring import *


@pytest.fixture
def mock_get_data(monkeypatch):
    def mock_download(ticker, period, interval):
        return pd.DataFrame({
            "Open": [100, 105, 110, 115, 120],
            "Close": [105, 110, 115, 120, 125],
            "High": [110, 115, 120, 125, 130],
            "Low": [95, 100, 105, 110, 115],
            "Volume": [100000, 110000, 120000, 130000, 140000]
        })
    monkeypatch.setattr("realtime_stock_monitoring.get_data", mock_download)

@pytest.fixture
def mock_train_models(monkeypatch):
    def mock_train():
        return [("rf", RandomForestClassifier()), ("xgb", XGBClassifier()), ("svm", SVC())]
    monkeypatch.setattr("realtime_stock_monitoring.train_models", mock_train)

def test_backtest(mock_get_data, mock_train_models):
    # Prepare mock data
    data = pd.DataFrame({
        "Open": [100, 105, 110, 115, 120],
        "Close": [105, 110, 115, 120, 125],
        "High": [110, 115, 120, 125, 130],
        "Low": [95, 100, 105, 110, 115],
        "Volume": [100000, 110000, 120000, 130000, 140000]
    })

    # Call the function to be tested
    models = train_models()
    preds, accuracy, precision = backtest(data, models)

    # Assertions
    assert isinstance(preds, np.ndarray)
    assert isinstance(accuracy, float)
    assert isinstance(precision, float)

    # Additional assertions based on your requirements
    # For example:
    # assert len(preds) == len(data) - train_size
    # assert accuracy >= 0.0 and accuracy <= 1.0
    # assert precision >= 0.0 and precision <= 1.0