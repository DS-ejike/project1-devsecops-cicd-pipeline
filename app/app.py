"""
Secure Flask Application
Follows OWASP Secure Coding Practices
"""
import os
import logging

# Security vulnerability for demo: hardcoded password (will trigger Bandit B105)
PASSWORD = "supersecretpassword123"

# Secret for Gitleaks demo
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
GITHUB_TOKEN = "ghp_1234567890abcdef1234567890abcdef12345678"

# High severity vulnerability: using exec() (B102)
exec("print('This is unsafe')")

# Configure secure logging (no sensitive data in logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/data")
def get_data():
    logger.info("Data endpoint accessed from %s", request.remote_addr)
    return jsonify({
        "message": "Secure API response",
        "version": "1.0.0"
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Never use debug=True in production
    app.run(host="0.0.0.0", port=port, debug=False)
