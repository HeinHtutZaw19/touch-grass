from flask import Blueprint, request, jsonify, current_app as app
from uuid import uuid4

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    res = app.supabase_client.table("users").select("*").execute()
    return jsonify(res.data)

@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    user = {
        "id": str(uuid4()),
        "name": data["name"],
        "photo_url": data.get("photo_url"),
        "datamap": {"analytical":0,"creative":0,"social":0,"practical":0}
    }
    res = app.supabase_client.table("users").insert(user).execute()
    return jsonify(res.data[0]), 201

@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    res = app.supabase_client.table("users").select("*").eq("id", user_id).execute()
    if not res.data:
        return jsonify({"error": "User not found"}), 404
    return jsonify(res.data[0])
