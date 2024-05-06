import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock


# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *
from widgets import *
from widgets import __login__

@pytest.fixture
def login_instance():
    return __login__(company_name="Test Company", width=200, height=200)

@patch('widgets.st')
def test_login_widget_success(mock_st, login_instance):
    st_session_state = {'LOGOUT_BUTTON_HIT': False, 'LOGGED_IN': False}
    with patch('widgets.check_usr_pass', return_value=True), \
         patch('widgets.__login__.cookies', MagicMock()):
        login_instance.login_widget()
        assert st_session_state['LOGGED_IN'] is True

@patch('widgets.st')
def test_login_widget_fail(mock_st, login_instance):
    st_session_state = {'LOGOUT_BUTTON_HIT': False, 'LOGGED_IN': False}
    with patch('widgets.check_usr_pass', return_value=False), \
         patch('widgets.__login__.cookies', MagicMock()):
        login_instance.login_widget()
        assert st_session_state['LOGGED_IN'] is False

@patch('widgets.st_lottie')
@patch('widgets.load_lottieurl', return_value={'animation': 'data'})
def test_animation(mock_load_lottieurl, mock_st_lottie, login_instance):
    login_instance.animation()
    mock_st_lottie.assert_called_once_with({'animation': 'data'}, width=200, height=200)

@patch('widgets.st.form')
def test_sign_up_widget_success(mock_form, login_instance):
    with patch('widgets.register_new_usr', return_value="Registration successful. Please check your email for confirmation."), \
         patch('widgets.send_registration_confirmation'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.sign_up_widget()

@patch('widgets.st.form')
def test_sign_up_widget_fail(mock_form, login_instance):
    with patch('widgets.st.error'), \
         patch('widgets.register_new_usr', return_value="Username already exists"), \
         patch('widgets.send_registration_confirmation'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.sign_up_widget()

@patch('widgets.st.form')
def test_forgot_password_success(mock_form, login_instance):
    with patch('widgets.check_email_exists', return_value=(True, 'test_user')), \
         patch('widgets.generate_random_passwd', return_value='random_password'), \
         patch('widgets.send_passwd_in_email'), \
         patch('widgets.change_passwd'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.forgot_password()

@patch('widgets.st.form')
def test_forgot_password_fail(mock_form, login_instance):
    with patch('widgets.st.error'), \
         patch('widgets.check_email_exists', return_value=(False, None)), \
         patch('widgets.generate_random_passwd', return_value='random_password'), \
         patch('widgets.send_passwd_in_email'), \
         patch('widgets.change_passwd'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.forgot_password()

@patch('widgets.st.form')
def test_reset_password_success(mock_form, login_instance):
    with patch('widgets.check_email_exists', return_value=(True, 'test_user')), \
         patch('widgets.check_current_passwd', return_value=True), \
         patch('widgets.change_passwd'), \
         patch('widgets.st.success'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.reset_password()

@patch('widgets.st.form')
def test_reset_password_fail(mock_form, login_instance):
    with patch('widgets.st.error'), \
         patch('widgets.check_email_exists', return_value=(False, None)), \
         patch('widgets.check_current_passwd', return_value=False), \
         patch('widgets.change_passwd'):
        mock_form.return_value.__enter__.return_value.form_submit_button.return_value = True
        login_instance.reset_password()

@patch('widgets.st.sidebar')
def test_logout_widget(mock_sidebar, login_instance):
    st_session_state = {'LOGGED_IN': True}
    with patch('widgets.st.sidebar.empty') as mock_empty:
        mock_empty.return_value.button.return_value = True
        login_instance.logout_widget()
        assert st_session_state['LOGGED_IN'] is False

@patch('widgets.st.sidebar.empty')
def test_nav_sidebar(mock_empty, login_instance):
    mock_empty.return_value.option_menu.return_value = 'Login'
    main_page_sidebar, selected_option = login_instance.nav_sidebar()
    assert selected_option == 'Login'

@patch('widgets.st.session_state', {'LOGGED_IN': False, 'LOGOUT_BUTTON_HIT': False})
@patch('widgets.st.sidebar.empty')
@patch('widgets.__login__.nav_sidebar')
@patch('widgets.__login__.login_widget')
@patch('widgets.__login__.animation')
@patch('widgets.__login__.sign_up_widget')
@patch('widgets.__login__.forgot_password')
@patch('widgets.__login__.reset_password')
@patch('widgets.__login__.logout_widget')
def test_build_login_ui(mock_logout_widget, mock_reset_password, mock_forgot_password, mock_sign_up_widget, mock_animation,
                        mock_login_widget, mock_nav_sidebar, mock_empty_sidebar, login_instance):
    mock_nav_sidebar.return_value = (mock_empty_sidebar, 'Login')
    assert login_instance.build_login_ui() is False
