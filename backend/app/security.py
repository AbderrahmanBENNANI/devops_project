from flask import request, jsonify

def install_security(app):
    @app.before_request
    def basic_api_guard():
        # En production, impose HTTPS via le tunnel et configure un secret fort.
        if request.path.startswith("/api/") and request.method not in ("GET", "POST", "OPTIONS"):
            return jsonify(error="method_not_allowed"), 405

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        return response
