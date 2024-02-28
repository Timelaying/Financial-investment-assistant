import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(
    page_title="Finance Adviser")

st.header("Finance Adviser")

__login__obj = __login__(
    auth_token = "pk_prod_0PP3FYA7VXMJ3EKZNB7R7SKWFWHR", # st.secrets.email_api_key
    company_name = "Finance Adviser",
    width = 200, height = 250, 
    logout_button_name = 'Logout', hide_menu_bool = False, 
    hide_footer_bool = False, 
    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:

    st.markdown("Your Streamlit Application Begins here!")