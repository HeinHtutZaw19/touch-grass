from flask import Blueprint, request, jsonify, current_app as app
from uuid import uuid4

hobbies_bp = Blueprint("hobbies", __name__)

@hobbies_bp.route("/", methods=["GET"])
def get_hobbies():
    res = app.supabase_client.table("hobbies").select("*").execute()
    return jsonify(res.data)

@hobbies_bp.route("/", methods=["POST"])
def create_hobby():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    hobby = {
        "id": str(uuid4()),
        "name": data["name"],
        "category": data.get("category"),
        "description": data.get("description")
    }
    res = app.supabase_client.table("hobbies").insert(hobby).execute()
    return jsonify(res.data[0]), 201
