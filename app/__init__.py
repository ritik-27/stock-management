from flask import Flask, jsonify
from mongoengine import connect
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    connect(host=app.config["MONGODB_URI"], db=app.config["MONGODB_DB_NAME"])

    from app.routes.product_routes import register_routes as product_register
    product_register(app)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found"}), 404

    return app
