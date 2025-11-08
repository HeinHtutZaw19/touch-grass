from flask import Blueprint, jsonify, request
from app.extensions import supabase_client

levels_bp = Blueprint("levels", __name__)

@levels_bp.route("/", methods=["GET"])
def get_levels():
    res = supabase_client.table("level_contents").select("*").execute()
    return jsonify(res.data), 200

@levels_bp.route("/", methods=["POST"])
def create_level():
    data = request.get_json()
    res = supabase_client.table("level_contents").insert(data).execute()
    return jsonify(res.data), 201
