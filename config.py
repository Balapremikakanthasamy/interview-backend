import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (if exists)
load_dotenv()

# Get base directory
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration shared across environments"""

    # Mail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"  # Optional SSL
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  # Needed for sessions

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR / 'interviews.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask settings
    DEBUG = False


class DevConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProdConfig(Config):
    """Production configuration"""
    DEBUG = False
