from flask import Blueprint, request, jsonify, current_app as app
from uuid import uuid4

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def list_users():
    try:
        res = app.supabase_client.table("users").select("*").execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    user_payload = {
        # optionally use provided id, otherwise DB will generate one
        "name": name,
        "photo_url": data.get("photo_url"),
        "mbti": data.get("mbti"),
        "personality_good": data.get("personality_good"),
        "personality_bad": data.get("personality_bad"),
        "suggested_careers": data.get("suggested_careers")
    }
    try:
        res = app.supabase_client.table("users").insert(user_payload).execute()
        created_user = res.data[0]
        dm_res = app.supabase_client.table("datamaps").insert({
            "user_id": created_user["id"],
            "analytical": 10,
            "creative": 0,
            "social": 0,
            "physical": 0
        }).execute()
        return jsonify(created_user), 201
    except Exception as e:
        return jsonify({"error": e}), 500



@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        res = app.supabase_client.table("users").select("*").eq("id", user_id).single().execute()
        if not res.data:
            return jsonify({"error": "User not found"}), 404
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json() or {}
    # only allow certain fields
    allowed = {"name","photo_url","mbti","personality_good","personality_bad","suggested_careers"}
    payload = {k: v for k, v in data.items() if k in allowed}
    if not payload:
        return jsonify({"error": "No valid fields to update"}), 400
    try:
        res = app.supabase_client.table("users").update(payload).eq("id", user_id).select("*").execute()
        if not res.data:
            return jsonify({"error": "User not found"}), 404
        return jsonify(res.data[0]), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        res = app.supabase_client.table("users").delete().eq("id", user_id).execute()
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": e}), 500
