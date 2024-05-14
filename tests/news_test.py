import streamlit as st  # Importing the Streamlit library for building web apps
import pytest  # Importing pytest for testing
import sys  # Importing sys for system-specific parameters and functions
import os  # Importing os for operating system dependent functionality
from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing
from unittest.mock import patch, MagicMock  # Importing patch and MagicMock for mocking

# Add parent directory to sys.path to ensure modules in the parent directory can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import custom module 'news' from the parent directory
from news import *

# Define a pytest fixture for mocking the get_news function
@pytest.fixture
def mock_get_news():
    with patch("news.get_news") as mock_get_news:
        yield mock_get_news

# Define a test function for rendering news
def test_render_news(mock_get_news):
    # Mocking the response of get_news function
    mock_get_news.return_value = [("Headline 1", "http://example.com/article1"), 
                                   ("Headline 2", "http://example.com/article2")]

    # Patching st.subheader and st.markdown
    with patch.object(st, "subheader"), patch.object(st, "markdown") as mock_markdown:
        # Calling the function under test
        render_news()

        # Asserting that st.subheader was called with "News"
        st.subheader.assert_called_once_with("News")

        # Asserting that st.markdown was called for each article with the correct HTML
        mock_markdown.assert_any_call('<a href="http://example.com/article1" style="font-size: 25px;">Headline 1</a>', unsafe_allow_html=True)
        mock_markdown.assert_any_call('<a href="http://example.com/article2" style="font-size: 25px;">Headline 2</a>', unsafe_allow_html=True)
