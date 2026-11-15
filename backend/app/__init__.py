import os
from flask import Flask, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .routes import api
from .security import install_security

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
LATENCY = Histogram("http_request_duration_seconds", "HTTP request duration")

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", "1048576"))
    app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY", "development-only-change-me")
    origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",") if x.strip()]
    CORS(app, resources={r"/api/*": {"origins": origins}}, methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])
    install_security(app)
    app.register_blueprint(api, url_prefix="/api/v1")

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="localfirst-api")

    @app.get("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    @app.errorhandler(413)
    def too_large(_):
        return jsonify(error="payload_too_large"), 413

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="not_found"), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify(error="internal_server_error"), 500

    return app
