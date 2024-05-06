import streamlit as st
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News as FinvizNews
from news import render_news as CNBC_news

def main_news():
    # List of ticker symbols
    tickers = ['GOOGL', 'GOOG', 'AAPL', 'JPM', 'BAC', 'MS', 'GS', 'BCS', 'MSFT', 'WFC', 'TSLA', 'UBS', 'EXPE', 'AMGN', 'NET', 'EVR']

    # Title and description
    st.title("Financial Investment Assistant")
    st.write("Welcome to the Financial Investment Assistant! This assistant provides tools and information to help you make informed investment decisions.")

    # Sidebar navigation
    menu = ["Home", "Stock Information", "Financial News", "CNBC News", "Insider Trading"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # Home page
    if choice == "Home":
        st.write("This assistant offers the following sections:")
        st.write("- Stock Information: Obtain detailed information about stocks.")
        st.write("- Financial News: Stay updated with financial news from FinvizFinance.")
        st.write("- CNBC News: Explore news from CNBC's World Markets section.")
        st.write("- Insider Trading: Get insights into insider trading activities.")
        
    # Stock Information page
    elif choice == "Stock Information":
        st.subheader("Get Stock Information")
        selected_ticker = st.selectbox("Select Ticker Symbol", tickers)
        if st.button("Get Information"):
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

    # Financial News page
    elif choice == "Financial News":
        st.subheader("Financial News")
        fnews = FinvizNews()
        all_news = fnews.get_news()
        selected_news = st.selectbox("Select News Type", ["news", "blogs"])
        if selected_news in all_news:
            st.write(all_news[selected_news].head())
        else:
            st.write("Selected news type not available.")

    # CNBC News page
    elif choice == "CNBC News":
        st.subheader("CNBC News")
        CNBC_news()

    # Insider Trading page
    elif choice == "Insider Trading":
        st.subheader("Insider Trading Information")
        insider_option = st.selectbox("Select Insider Option", ["latest", "top week", "top owner trade"])
        finsider = Insider(option=insider_option)
        insider_trader = finsider.get_insider()
        st.write(insider_trader)

if __name__ == "__main__":
    main_news()
