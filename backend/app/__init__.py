from flask import Flask
import os
from flask import Blueprint, request, jsonify, current_app as app
from uuid import uuid4


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_mapping(
        SUPABASE_URL=os.getenv("SUPABASE_URL"),
        SUPABASE_KEY=os.getenv("SUPABASE_KEY")
    )
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "message": "Touch Grass API is running"
        })

    # Import and register API blueprints
    from app.api.users import users_bp
    from app.api.hobbies import hobbies_bp
    from app.api.exercises import exercises_bp

    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(hobbies_bp, url_prefix="/api/hobbies")
    app.register_blueprint(exercises_bp, url_prefix="/api/exercises")

    return app
