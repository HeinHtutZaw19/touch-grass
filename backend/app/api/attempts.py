from flask import Blueprint, jsonify, request
from app.extensions import supabase_client

attempts_bp = Blueprint("attempts", __name__)

@attempts_bp.route("/", methods=["GET"])
def get_attempts():
    res = supabase_client.table("exercise_attempts").select("*").execute()
    return jsonify(res.data), 200

@attempts_bp.route("/", methods=["POST"])
def create_attempt():
    data = request.get_json()
    res = supabase_client.table("exercise_attempts").insert(data).execute()
    return jsonify(res.data), 201
