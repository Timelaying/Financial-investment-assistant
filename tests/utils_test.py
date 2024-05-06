import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock


# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import utils
from utils import *


def test_check_usr_pass():
    # Assuming _secret_auth_.json contains user data
    assert check_usr_pass("username", "password")


def test_check_valid_name():
    assert check_valid_name("Valid_Name")


def test_check_valid_email():
    assert check_valid_email("example@example.com")
    assert not check_valid_email("invalid_email")


def test_check_unique_email():
    # Assuming the provided email is unique
    assert check_unique_email("new@example.com")


def test_non_empty_str_check():
    assert non_empty_str_check("Non-empty string")
    assert not non_empty_str_check("")


def test_check_unique_usr():
    # Assuming the provided username is unique and non-empty
    assert check_unique_usr("new_username")


def test_register_new_usr():
    # Assuming valid data provided for registration
    assert register_new_usr("Name", "email@example.com", "username", "password") == "Registration successful. Please check your email for confirmation."


def test_check_email_exists():
    # Assuming the provided email exists in the database
    assert check_email_exists("email@example.com")


def test_generate_random_passwd():
    assert len(generate_random_passwd()) == 14


# Define mock function for sending email since we don't want to send actual emails during testing
def mock_send_email(email):
    pass


def test_send_registration_confirmation(monkeypatch):
    monkeypatch.setattr("utils.send_registration_confirmation", mock_send_email)
    send_registration_confirmation("email@example.com")


def test_send_passwd_in_email(monkeypatch):
    monkeypatch.setattr("utils.send_passwd_in_email", mock_send_email)
    send_passwd_in_email("username", "email@example.com", "Company", "random_password")


def test_send_registration_confirmation():
    # Mocking smtplib.SMTP to prevent actual email sending
    with patch("smtplib.SMTP") as mock_smtp:
        send_registration_confirmation("email@example.com")
        mock_smtp.assert_called_once()


def test_send_passwd_in_email():
    # Mocking smtplib.SMTP to prevent actual email sending
    with patch("smtplib.SMTP") as mock_smtp:
        send_passwd_in_email("username", "email@example.com", "Company", "random_password")
        mock_smtp.assert_called_once()
