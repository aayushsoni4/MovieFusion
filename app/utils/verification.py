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
    Sends a personalized email containing a one-time password (OTP) for account verification.

    Args:
        email (str): The email address of the new user.
        token (str): The verification token.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Generate a new OTP token for the email
        token = otp.now()

        # Personalized subject line
        subject = "Welcome to MovieFusion! Let's Get Started"

        # HTML email body with engaging content and formatting
        message_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .container {{
                    font-family: Arial, sans-serif;
                    margin: 0 auto;
                    padding: 20px;
                    max-width: 600px;
                    background-color: #f9f9f9;
                    border: 1px solid #e70634;
                    border-radius: 10px;
                }}
                .header {{
                    color: #e70634;
                    text-align: center;
                }}
                .otp {{
                    font-size: 24px;
                    text-align: center;
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #fff;
                    border: 1px solid #e70634;
                    border-radius: 5px;
                    display: inline-block;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #555;
                }}
                .footer a {{
                    color: #e70634;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="header">Welcome to MovieFusion!</h2>
                <p>Thank you for joining our movie streaming platform with a personalized recommendation system.
                    We're excited to help you discover your next favorite film!</p>

                <p>To complete your registration, please enter the following OTP:</p>
                <div class="otp">{token}</div>

                <p>This OTP is valid for 5 minutes. If you don't verify your account within this time, you can request a new OTP.</p>

                <p>We hope you enjoy your MovieFusion experience!</p>

                <div class="footer">
                    <p>Best regards,<br>
                    The MovieFusion Team</p>
                    <p><a href="https://github.com/aayushsoni4/MovieFusion">Visit MovieFusion</a></p>
                </div>
            </div>
        </body>
        </html>
        """

        msg = Message(
            subject, recipients=[email], html=message_body
        )  # Use HTML format for the email body
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
