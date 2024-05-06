import news  # assuming your code is in a file named main.py
import streamlit as st
import pytest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_get_news():
    with patch("news.get_news") as mock_get_news:
        yield mock_get_news

def test_render_news(mock_get_news):
    # Mocking the response of get_news function
    mock_get_news.return_value = [("Headline 1", "http://example.com/article1"), 
                                   ("Headline 2", "http://example.com/article2")]

    # Patching st.subheader and st.markdown
    with patch.object(st, "subheader"), patch.object(st, "markdown") as mock_markdown:
        # Calling the function under test
        news.render_news()

        # Asserting that st.subheader was called
        st.subheader.assert_called_once_with("News")

        # Asserting that st.markdown was called for each article
        mock_markdown.assert_any_call('<a href="http://example.com/article1" style="font-size: 25px;">Headline 1</a>', unsafe_allow_html=True)
        mock_markdown.assert_any_call('<a href="http://example.com/article2" style="font-size: 25px;">Headline 2</a>', unsafe_allow_html=True)
