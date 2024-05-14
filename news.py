import requests
from bs4 import BeautifulSoup
import streamlit as st

# Cache the function to improve performance
@st.cache
def get_news():
    # Define the URL to scrape
    url = 'https://www.cnbc.com/world-markets/'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all anchor tags with class 'Card-title' which contain the headlines and links
    articles = soup.find_all('a', href=True, class_='Card-title')
    
    # Extract headlines and links from the anchor tags
    news = []
    for article in articles:
        headline = article.text.strip()  # Extract headline text
        link = article['href']  # Extract the URL
        news.append((headline, link))  # Append headline and link as tuple to the news list
    return news

# Function to render news in Streamlit
def render_news():
    # Call the get_news function to retrieve headlines and links
    news = get_news()
    
    # Display news section header
    st.subheader("News")
    
    # Iterate over each headline-link pair and render them
    for headline, link in news:
        # Create a styled HTML link using Markdown syntax
        styled_link = f'<a href="{link}" style="font-size: 25px;">{headline}</a>'
        
        # Render the styled link in Streamlit
        st.markdown(styled_link, unsafe_allow_html=True)
        
        # Add an empty line for spacing
        st.write("")
