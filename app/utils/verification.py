from flask_mail import Message
from flask import url_for
from dotenv import load_dotenv
from logger import logger
from app import db, mail
from app.models import User
import secrets
import pyotp
import os

# Load environment variables from a .env file
load_dotenv()

# Initialize TOTP with a secret key and a time interval of 300 seconds (5 minutes)
otp = pyotp.TOTP(os.getenv("otp_key"), interval=300)


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
    # Validate username and password
    if not username or not password:
        logger.error("Invalid username or password provided.")
        return False

    try:
        # Create a new user instance and add it to the 'users' table
        user = User(username=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"User '{username}' added to 'users' table.")
        return True
    except Exception as e:
        # Log any exception that occurs
        logger.error(f"Error adding user to 'users' table: {e}")
        return False


def send_otp(email):
    """
    Send a one-time password (OTP) for email verification.

    Args:
        email (str): The email address to which the OTP will be sent.

    Returns:
        bool: True if the OTP is sent successfully, False otherwise.
    """
    try:
        # Generate a one-time password (OTP)
        totp_value = otp.now()

        # Create an email message with the OTP
        message = Message("Your OTP for Verification", recipients=[email])
        message.body = f"Your OTP is: {totp_value}"

        # Send the email
        mail.send(message)
        logger.info(f"OTP sent successfully to {email}.")
        return True
    except Exception as e:
        # Log any exception that occurs
        logger.error(f"Error sending OTP to {email}: {e}")
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
        # Query the 'users' table for the user by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Set the user's 'is_activated' status to True and commit the change
            user.is_activated = True
            db.session.commit()
            logger.info(f"User '{user.username}' activated in 'users' table.")
            return True
        else:
            # Log a warning if the user is not found
            logger.warning(f"User with email '{email}' not found.")
            return None
    except Exception as e:
        # Log any exception that occurs
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
    # Construct the reset link with the token
    reset_link = url_for("auth.reset_password", token=token, _external=True)

    try:
        # Create a message with the reset link
        message = Message("Password Reset", recipients=[email])
        message.body = f"Click the following link to reset your password: {reset_link}"

        # Send the email
        mail.send(message)
        logger.info(f"Password reset email sent successfully to {email}.")
        return True
    except Exception as e:
        # Log any exception that occurs
        logger.error(f"Error sending password reset email to {email}: {e}")
        return False
