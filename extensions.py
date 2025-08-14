# backend/extensions.py

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions (do not bind to app yet)
mail = Mail()
db = SQLAlchemy()  # Added for future database integration
