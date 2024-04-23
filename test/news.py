import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache
def get_news():
    url = 'https://www.cnbc.com/world-markets/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all('a', href=True, class_='Card-title')
    
    news = []
    for article in articles:
        headline = article.text.strip()
        link = article['href']
        news.append((headline, link))
    return news

def render_news():
    news = get_news()
    st.subheader("News")
    for headline, link in news:
        styled_link = f'<a href="{link}" style="font-size: 25px;">{headline}</a>'
        st.markdown(styled_link, unsafe_allow_html=True)
        st.write("")


