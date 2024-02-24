import streamlit as st
from streamlit_login_auth_ui.widgets import _login_

st.set_page_config(
    page_title="Finance Adviser")

st.header("Finance Adviser")

_loginobj = __login_(
    auth_token = st.secrets.email_api_key,
    company_name = "Finance Adviser",
    width = 200, height = 250, 
    logout_button_name = 'Logout', hide_menu_bool = False, 
    hide_footer_bool = False, 
    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = _login_obj.build_login_ui()

if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")
