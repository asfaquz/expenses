import logging

logger = logging.getLogger(__name__)

def send_welcome_email(user_email, user_name):
    """
    Log a welcome email to the new user instead of actually sending it.
    """
    subject = "Welcome to Expenses Management System"
    message = f"Hello {user_name},\n\nWelcome to our platform! We're glad to have you."
    from_email = "no-reply@example.com"  # Change as needed
    recipient_list = [user_email]

    logger.info(
        f"[MOCK EMAIL] To: {recipient_list} | Subject: {subject} | From: {from_email} | Message: {message}"
    )