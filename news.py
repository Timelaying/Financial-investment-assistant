import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import streamlit as st

@st.cache_data
def get_news():
    link_list = []
    headline_list = []
    url = 'https://www.cnbc.com/world-markets/'
    get_url = requests.get(url)
    soup = BeautifulSoup(get_url.text, "html.parser")
    links = [link.get('href') for link in soup.find_all('a')]
    links = [link for link in links if link and link.startswith('https://www.cnbc.com/2024/')]

    # Function to normalize URLs for comparison
    def normalize_url(url):
        parsed_url = urlparse(url)
        return parsed_url.geturl()

    links = list(set(normalize_url(link) for link in links))

    for link in links:
        get_url = requests.get(link)
        soup = BeautifulSoup(get_url.text, "html.parser")
        headline = soup.select('h1.ArticleHeader-headline')
        if len(headline) > 0:
            headline = headline[0].get_text()
            link_list.append(link)
            headline_list.append(headline)
            zipped_list = zip(link_list, headline_list)
    return zipped_list

def render_news():
    news = get_news()
    st.subheader("News")
    for link, headline in news:
        styled_link = f'<a href="{link}" style="font-size: 25px;">{headline}</a>'
        st.markdown(styled_link, unsafe_allow_html=True)
        st.write("")
