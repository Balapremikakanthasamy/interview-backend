from flask_mail import Message
from extensions import mail
import logging

def send_email(subject, recipients, body):
    """Send an email using Flask-Mail."""
    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)
        logging.info(f"✅ Email sent successfully to: {recipients}")
        return True
    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")
        return False
