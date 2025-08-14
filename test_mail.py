# backend/test_mail.py
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Mail configuration from .env
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

with app.app_context():
    try:
        recipient_email = "candidate_email@gmail.com"  # Change to a real test email
        msg = Message(
            subject="Test Email",
            recipients=[recipient_email],
            body="Hello! This is a test email from Flask."
        )
        mail.send(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error:", e)
