import sys  # Importing sys for system-specific parameters and functions
import os  # Importing os for operating system dependent functionality
import json  # Importing json for JSON parsing
import pytest  # Importing pytest for testing
from unittest.mock import patch, MagicMock  # Importing patch and MagicMock for mocking

# Add parent directory to sys.path to ensure modules in the parent directory can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import custom module 'utils' from the parent directory
from utils import *


# Test the check_usr_pass function
def test_check_usr_pass():
    # Assuming _secret_auth_.json contains user data
    assert check_usr_pass("username", "password")


# Test the check_valid_name function
def test_check_valid_name():
    assert check_valid_name("Valid_Name")


# Test the check_valid_email function
def test_check_valid_email():
    assert check_valid_email("example@example.com")
    assert not check_valid_email("invalid_email")


# Test the check_unique_email function
def test_check_unique_email():
    # Assuming the provided email is unique
    assert check_unique_email("new@example.com")


# Test the non_empty_str_check function
def test_non_empty_str_check():
    assert non_empty_str_check("Non-empty string")
    assert not non_empty_str_check("")


# Test the check_unique_usr function
def test_check_unique_usr():
    # Assuming the provided username is unique and non-empty
    assert check_unique_usr("new_username")


# Test the register_new_usr function
def test_register_new_usr():
    # Assuming valid data provided for registration
    assert register_new_usr("Name", "email@example.com", "username", "password") == "Registration successful. Please check your email for confirmation."


# Test the check_email_exists function
def test_check_email_exists():
    # Assuming the provided email exists in the database
    assert check_email_exists("email@example.com")


# Test the generate_random_passwd function
def test_generate_random_passwd():
    assert len(generate_random_passwd()) == 14


# Define mock function for sending email since we don't want to send actual emails during testing
def mock_send_email(email):
    pass


# Test the send_registration_confirmation function with mocked email sending
def test_send_registration_confirmation(monkeypatch):
    monkeypatch.setattr("utils.send_registration_confirmation", mock_send_email)
    send_registration_confirmation("email@example.com")


# Test the send_passwd_in_email function with mocked email sending
def test_send_passwd_in_email(monkeypatch):
    monkeypatch.setattr("utils.send_passwd_in_email", mock_send_email)
    send_passwd_in_email("username", "email@example.com", "Company", "random_password")


# Test the send_registration_confirmation function by mocking smtplib.SMTP to prevent actual email sending
def test_send_registration_confirmation():
    # Mocking smtplib.SMTP to prevent actual email sending
    with patch("smtplib.SMTP") as mock_smtp:
        send_registration_confirmation("email@example.com")
        mock_smtp.assert_called_once()


# Test the send_passwd_in_email function by mocking smtplib.SMTP to prevent actual email sending
def test_send_passwd_in_email():
    # Mocking smtplib.SMTP to prevent actual email sending
    with patch("smtplib.SMTP") as mock_smtp:
        send_passwd_in_email("username", "email@example.com", "Company", "random_password")
        mock_smtp.assert_called_once()
