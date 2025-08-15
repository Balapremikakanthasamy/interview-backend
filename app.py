from flask import Flask, send_from_directory
from flask_cors import CORS
from extensions import mail, db
import logging
from routes.interview_routes import interview_bp
import os

def create_app():
    app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
    app.config.from_object("config.ProdConfig")

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)

    # Enable CORS for all routes and all origins (testing mode)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("✅ Flask app initialized")

    # Create DB tables
    with app.app_context():
        db.create_all()
        app.logger.info("📂 Database tables created")

    # Register Blueprints
    app.register_blueprint(interview_bp, url_prefix="/api/interview")
    app.logger.debug("📅 Interview routes registered")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "success", "message": "Backend is running"}

    # Serve React build
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
