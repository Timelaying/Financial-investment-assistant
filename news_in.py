import streamlit as st
from finvizfinance.news import News as FinvizNews
from news import render_news as CNBC_news  # Importing a function from a local module
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider

@st.cache_data(ttl=600, show_spinner=False)
def _finviz_news():
    return FinvizNews().get_news()


@st.cache_data(ttl=600, show_spinner=False)
def _finviz_insider(option):
    return Insider(option=option).get_insider()


def _unavailable(what):
    st.info(f"{what} is temporarily unavailable. The data source may be limiting requests from this host; please try again later.")


def main_news():
    # List of ticker symbols
    tickers = ['GOOGL', 'GOOG', 'AAPL', 'JPM', 'BAC', 'MS', 'GS', 'BCS', 'MSFT', 'WFC', 'TSLA', 'UBS', 'EXPE', 'AMGN', 'NET', 'EVR']

    # Title and description
    st.title("Financial Investment Assistant")
    st.write("Welcome to the Financial Investment Assistant! This assistant provides tools and information to help you make informed investment decisions.")

    # Navigation options as radio buttons
    st.header("Navigation")
    selected_option = st.radio("Section", ["Home", "Stock Information", "Financial News", "CNBC News", "Insider Trading"], label_visibility="collapsed")

    # Home page
    if selected_option == "Home":
        st.write("This assistant offers the following sections:")
        st.write("- Stock Information: Obtain detailed information about stocks.")
        st.write("- Financial News: Stay updated with financial news from FinvizFinance.")
        st.write("- CNBC News: Explore news from CNBC's World Markets section.")
        st.write("- Insider Trading: Get insights into insider trading activities.")
        
    # Stock Information page
    elif selected_option == "Stock Information":
        st.subheader("Get Stock Information")
        selected_ticker = st.selectbox("Select Ticker Symbol", tickers)
        if st.button("Get Information"):
            try:
                stock = finvizfinance(selected_ticker)
                st.subheader("Stock Charts")
                stock.ticker_charts()
            
                st.subheader("Fundamental Information")
                stock_fundament = stock.ticker_fundament()
                st.write(stock_fundament)
            
                st.subheader("Description")
                stock_description = stock.ticker_description()
                st.write(stock_description)
            
                st.subheader("Outer Ratings")
                outer_ratings_df = stock.ticker_outer_ratings()
                st.write(outer_ratings_df)
            
                st.subheader("Stock News")
                news_df = stock.ticker_news()
                st.write(news_df)
            
                st.subheader("Inside Trader")
                inside_trader_df = stock.ticker_inside_trader()
                st.write(inside_trader_df)
            except Exception:  # noqa: BLE001
                _unavailable("Stock information")

    # Financial News page
    elif selected_option == "Financial News":
        st.subheader("Financial News")
        try:
            all_news = _finviz_news()
        except Exception:  # noqa: BLE001
            _unavailable("Financial news")
        else:
            selected_news = st.selectbox("Select News Type", ["news", "blogs"])
            if selected_news in all_news:
                st.write(all_news[selected_news].head())
            else:
                st.write("Selected news type not available.")

    # CNBC News page
    elif selected_option == "CNBC News":
        st.subheader("CNBC News")
        try:
            CNBC_news()  # Calling a function to render CNBC news
        except Exception:  # noqa: BLE001
            _unavailable("CNBC news")

    # Insider Trading page
    elif selected_option == "Insider Trading":
        st.subheader("Insider Trading Information")
        insider_option = st.selectbox("Select Insider Option", ["latest", "top week", "top owner trade"])
        try:
            st.write(_finviz_insider(insider_option))
        except Exception:  # noqa: BLE001
            _unavailable("Insider trading data")

if __name__ == "__main__":
    main_news()
