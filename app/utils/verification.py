from flask_mail import Message
from flask import url_for, render_template
from dotenv import load_dotenv
from logger import logger
from app import db, mail
from app.models import User
import secrets
# import pyotp
# import os

# Load environment variables from a .env file
load_dotenv()

# Initialize TOTP with a secret key and a time interval of 300 seconds (5 minutes)
# otp = pyotp.TOTP(os.getenv("OTP_KEY"), interval=300)


def add_user(username, email, password):
    """
    Add a new user to the 'users' table.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The hashed password of the user.

    Returns:
        bool: True if the user is successfully added, False otherwise.
    """
    if not username or not password:
        logger.error("Invalid username or password provided.")
        return False

    try:
        user = User(username=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"User '{username}' added to 'users' table.")
        return True
    except Exception as e:
        logger.error(f"Error adding user to 'users' table: {e}")
        return False


def send_otp(email):
    """
    Sends a personalized email containing a one-time password (OTP) for account verification.

    Args:
        email (str): The email address of the new user.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        token = 784941
        # token = otp.now()
        subject = "Welcome to MovieFusion! Let's Get Started"
        message_body = render_template("email/otp_email.html", token=token)
        msg = Message(subject, recipients=[email], html=message_body)
        mail.send(msg)
        logger.info(f"Verification email sent successfully to {email}.")
        return True
    except Exception as e:
        logger.error(f"Error sending verification email to {email}: {e}")
        return False


def generate_token():
    """
    Generate a secure token.

    Returns:
        str: A securely generated token.
    """
    return secrets.token_urlsafe(32)


def activate_user(email):
    """
    Activate a user for the specified email.

    Args:
        email (str): The email of the user to be activated.

    Returns:
        bool or None: True if the user is activated, None if the user is not found.
    """
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_activated = True
            db.session.commit()
            logger.info(f"User '{user.username}' activated in 'users' table.")
            return True
        else:
            logger.warning(f"User with email '{email}' not found.")
            return None
    except Exception as e:
        logger.error(f"Error activating user in 'users' table: {e}")
        return None


def send_password_reset_email(email, token):
    """
    Send a password reset email containing the reset link with the token.

    Args:
        email (str): The email address of the user.
        token (str): The unique token for password reset.

    Returns:
        bool: True if the email is sent successfully, False otherwise.
    """
    reset_link = url_for("auth.reset_password", token=token, _external=True)
    try:
        subject = "Password Reset Request for MovieFusion"
        message_body = render_template(
            "email/password_reset_email.html", reset_link=reset_link
        )

        msg = Message(subject, recipients=[email], html=message_body)
        mail.send(msg)
        logger.info(f"Password reset email sent successfully to {email}.")
        return True
    except Exception as e:
        logger.error(f"Error sending password reset email to {email}: {e}")
        return False
