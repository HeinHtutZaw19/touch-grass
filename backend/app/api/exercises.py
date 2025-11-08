from flask import Blueprint, jsonify, request
from app.extensions import supabase_client

exercises_bp = Blueprint("exercises", __name__)

@exercises_bp.route("/", methods=["GET"])
def get_exercises():
    res = supabase_client.table("exercises").select("*").execute()
    return jsonify(res.data), 200

@exercises_bp.route("/", methods=["POST"])
def create_exercise():
    data = request.get_json()
    res = supabase_client.table("exercises").insert(data).execute()
    return jsonify(res.data), 201
