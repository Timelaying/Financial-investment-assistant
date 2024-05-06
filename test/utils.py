import re
import requests
import json
import secrets
from argon2 import PasswordHasher
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ph = PasswordHasher() 

def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    for registered_user in authorized_user_data:
        if registered_user['username'] == username:
            try:
                passwd_verification_bool = ph.verify(registered_user['password'], password)
                if passwd_verification_bool:
                    return True
            except:
                pass
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(e)
    return None


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = r'^[A-Za-z_][A-Za-z0-9_]*'

    return re.match(name_regex, name_sign_up) is not None


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    return bool(re.fullmatch(regex, email_sign_up))


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)
        existing_emails = [user['email'] for user in authorized_users_data]

    return email_sign_up not in existing_emails


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    return bool(username_sign_up.strip())


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)
        existing_usernames = [user['username'] for user in authorized_users_data]

    if username_sign_up in existing_usernames:
        return False
    
    return non_empty_str_check(username_sign_up)


def register_new_usr(name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> str:
    """
    Saves the information of the new user in the _secret_auth_.json file.
    """
    new_usr_data = {'username': username_sign_up, 'name': name_sign_up, 'email': email_sign_up, 'password': ph.hash(password_sign_up)}

    try:
        with open("_secret_auth_.json", "r") as auth_json:
            authorized_user_data = json.load(auth_json)
    except FileNotFoundError:
        authorized_user_data = []

    authorized_user_data.append(new_usr_data)

    with open("_secret_auth_.json", "w") as auth_json_write:
        json.dump(authorized_user_data, auth_json_write)

    return "Registration successful. Please check your email for confirmation."

def send_registration_confirmation(email: str) -> None:
    """
    Sends a registration confirmation email to the user.
    """
    # Email content
    subject = "Registration Confirmation"
    message = "Thank you for registering with us!"

    # Create message
    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"  # Your email address
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Send email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # or 465 for SSL
    smtp_username = 'makanjuola.timi@gmail.com'
    smtp_password = 'taoy llcp jiio kjqx'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())


def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth_.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    for user in authorized_users_data:
        if user['email'] == email_forgot_passwd:
            return True, user['username']
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str) -> None:
    """
    Sends the randomly generated password to the user's email.
    """
    # Configure SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # or 465 for SSL
    smtp_username = 'makanjuola.timi@gmail.com'
    smtp_password = 'taoy llcp jiio kjqx'
    
    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email_forgot_passwd
    msg['Subject'] = f'{company_name}: Login Password!'
    body = f"Hi {username_forgot_passwd},\n\nYour temporary login password is: {random_password}\n\nPlease reset your password at the earliest for security reasons."
    msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email_forgot_passwd, msg.as_string())


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    for user in authorized_users_data:
        if user['email'] == email_:
            user['password'] = ph.hash(random_password)

    with open("_secret_auth_.json", "w") as auth_json_:
        json.dump(authorized_users_data, auth_json_)


def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when 
    resetting the password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    for user in authorized_users_data:
        if user['email'] == email_reset_passwd:
            try:
                if ph.verify(user['password'], current_passwd):
                    return True
            except:
                pass
    return False
