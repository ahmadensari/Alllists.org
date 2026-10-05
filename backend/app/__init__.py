import logging

from flask import Flask, jsonify

from .config import load_config
from .models import db


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.update(load_config())
    if overrides:
        app.config.update(overrides)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    db.init_app(app)

    from .routes import auth, lists, payments

    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(lists.bp, url_prefix="/api/lists")
    app.register_blueprint(payments.bp, url_prefix="/api/payments")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.cli.command("init-db")
    def init_db():
        """Create any missing tables."""
        db.create_all()
        print("Database tables are ready.")

    return app
