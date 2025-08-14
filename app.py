from flask import Flask
from flask_cors import CORS
from config import DevConfig
from extensions import mail, db
import logging


def create_app():
    """Application factory for creating Flask app"""
    app = Flask(__name__)

    # Load config
    app.config.from_object(DevConfig)

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True
    )

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    app.logger.info("✅ Flask application initialized")

    # Create database tables automatically (development only)
    with app.app_context():
        db.create_all()
        app.logger.info("📂 Database tables created (if not existing)")

    # Register Blueprints
    from routes.mail_routes import mail_bp
    from routes.interview_routes import interview_bp

    app.register_blueprint(mail_bp, url_prefix="/mail")
    app.logger.debug("📩 Mail routes registered")

    app.register_blueprint(interview_bp, url_prefix='/api/interview')
    app.logger.debug("📅 Interview routes registered")

    # Root health check
    @app.route('/')
    def index():
        return {"status": "success", "message": "Interview Scheduler Backend is running"}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
