import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

# Set page configuration
st.set_page_config(
    page_title="Finance Adviser",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for improved UI with sky blue background color
st.markdown("""
    <style>
    .stApp {
        background-color: #87CEEB; /* Sky blue */
    }
    .st-hv > div:first-child {
        background-color: #1e88e5;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
    }
    .st-hv > div:first-child h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 10px;
    }
    .st-hv > div:first-child p {
        color: white;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .st-hv > div:last-child {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .st-hv > div:last-child button {
        background-color: #1e88e5;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .st-hv > div:last-child button:hover {
        background-color: #1565c0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<div style='text-align: center;'><h1>Finance Adviser</h1><p>Your trusted financial assistant</p></div>", unsafe_allow_html=True)

# Initialize Login widget
__login__obj = __login__(
    auth_token="pk_prod_0PP3FYA7VXMJ3EKZNB7R7SKWFWHR",  # Replace with your auth token or st.secrets.email_api_key
    company_name="Finance Adviser",
    width=300,
    height=400,
    logout_button_name='Logout',
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

# Display login UI
LOGGED_IN = __login__obj.build_login_ui()

# Display success message if logged in, otherwise display warning message
if LOGGED_IN:
    st.success("You are logged in! Welcome to Finance Adviser.")
else:
    st.warning("Please log in to access Finance Adviser.")
