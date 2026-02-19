# Financial Investment Assistant

The Financial Investment Assistant is a Python application that helps investors make informed decisions by combining portfolio management, real‑time market data, news sentiment analysis and trading simulation into a single toolkit. It’s designed for individual investors to track performance, explore trading strategies and monitor market trends without needing deep technical knowledge.

## Features

- **Portfolio management** – add, update and track your investment holdings, with performance calculations and diversification metrics.
- **Real‑time stock monitoring** – fetch current stock prices and key financial indicators from external APIs.
- **News sentiment analysis** – analyze financial news headlines to gauge positive or negative sentiment around tickers.
- **Trading simulator** – practice strategies using historical data and simulated trades to see potential outcomes.
- **Recommendations** – generate simple investment recommendations based on risk tolerance and market conditions.

## Tech Stack

- **Language:** Python 3
- **Libraries:** Streamlit, Pandas, NumPy, Matplotlib / Plotly, yfinance or Alpha Vantage API
- **Database:** SQLite (for local data persistence)
- **Tools:** Docker (optional for containerisation), GitHub Actions for CI

## Architecture

This project follows a modular structure:

- `app.py` – main Streamlit application entrypoint for the user interface.
- `portfolio_management.py` – functions for managing and analysing a portfolio.
- `trading_simulator.py` – simulation engine for executing hypothetical trades.
- `realtime_stock_monitoring.py` – utilities for fetching live market data.
- `news_in.py` & `recommendation_results.py` – sentiment analysis and recommendation logic.
- `reading_resources.py` and `widgets.py` – helper functions and UI components.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- (Optional) An API key for stock data providers (e.g. Alpha Vantage)

### Installation

```bash
# Clone the repository
git clone https://github.com/Timelaying/Financial-investment-assistant.git
cd Financial-investment-assistant

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys (if needed)
cp .env.example .env
# edit .env with your API key
```

### Running the App

```bash
# Launch the Streamlit web app
streamlit run app.py
```

Access the app in your browser at `http://localhost:8501`. Use the sidebar to manage your portfolio, run simulations and view market data.

## Tests

Unit tests are located in the `tests/` directory and can be run with:

```bash
pytest
```

## Roadmap

- Incorporate more data sources and asset types (e.g., ETFs, crypto).
- Add charts and interactive dashboards for deeper analysis.
- Implement machine learning models for predictive analytics.
- Expand the trading simulator to support options and short selling.

## Contributing

Contributions are welcome! To propose improvements or report bugs, please open an issue. Fork the repository and submit a pull request describing your changes. Ensure code is formatted and tested before submitting.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
