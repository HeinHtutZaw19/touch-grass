from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime

hobbies_bp = Blueprint("hobbies", __name__)

@hobbies_bp.route("/", methods=["GET"])
def list_hobbies():
    try:
        res = app.supabase_client.table("hobbies").select("*").execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@hobbies_bp.route("/", methods=["POST"])
def create_hobby():
    data = request.get_json() or {}
    name = data.get("name")
    category = data.get("category")
    if not name or not category:
        return jsonify({"error":"name and category required"}), 400

    payload = {
        "name": name,
        "category": category,
        "description": data.get("description")
    }
    try:
        res = app.supabase_client.table("hobby").insert(payload).select("*").execute()
        return jsonify(res.data[0]), 201
    except Exception as e:
        return jsonify({"error": e}), 500

@hobbies_bp.route("/<hobby_id>", methods=["GET"])
def get_hobby(hobby_id):
    try:
        res = app.supabase_client.table("hobbies").select("*").eq("id", hobby_id).single().execute()
        if not res.data:
            return jsonify({"error": "Hobby not found"}), 404
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@hobbies_bp.route("/<hobby_id>", methods=["PATCH"])
def update_hobby(hobby_id):
    data = request.get_json() or {}
    allowed = {"name","category","description"}
    payload = {k: v for k,v in data.items() if k in allowed}
    if not payload:
        return jsonify({"error":"no valid fields"}), 400
    try:
        res = app.supabase_client.table("hobbies").update(payload).eq("id", hobby_id).select("*").execute()
        return jsonify(res.data[0]), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@hobbies_bp.route("/<hobby_id>", methods=["DELETE"])
def delete_hobby(hobby_id):
    try:
        res = app.supabase_client.table("hobbies").delete().eq("id", hobby_id).execute()
        return jsonify({"deleted": True}), 200
    except Exception as e: 
        return jsonify({"error": e}), 500
