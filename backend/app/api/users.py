from flask import Blueprint, request, jsonify, current_app as app
from uuid import uuid4

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def list_users():
    res = app.supabase_client.table("users").select("*").execute()
    if res.error:
        return jsonify({"error": str(res.error)}), 500
    return jsonify(res.data), 200

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

    res = app.supabase_client.table("users").insert(user_payload).execute()
    if res.error:
        return jsonify({"error": str(res.error)}), 500

    created_user = res.data[0]

    # Ensure a datamap exists for this user
    dm_res = app.supabase_client.table("datamaps").insert({
        "user_id": created_user["id"],
        "analytical": 0,
        "creative": 0,
        "social": 0,
        "physical": 0
    }).execute()

    # ignore datamap errors (but log)
    if dm_res.error:
        app.logger.warning("Failed to create datamap for user %s: %s", created_user["id"], dm_res.error)

    return jsonify(created_user), 201

@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    res = app.supabase_client.table("users").select("*").eq("id", user_id).single().execute()
    if res.error:
        return jsonify({"error": str(res.error)}), 500
    if not res.data:
        return jsonify({"error": "User not found"}), 404
    return jsonify(res.data), 200

@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json() or {}
    # only allow certain fields
    allowed = {"name","photo_url","mbti","personality_good","personality_bad","suggested_careers"}
    payload = {k: v for k, v in data.items() if k in allowed}
    if not payload:
        return jsonify({"error": "No valid fields to update"}), 400

    res = app.supabase_client.table("users").update(payload).eq("id", user_id).select("*").execute()
    if res.error:
        return jsonify({"error": str(res.error)}), 500
    if not res.data:
        return jsonify({"error": "User not found"}), 404
    return jsonify(res.data[0]), 200

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    res = app.supabase_client.table("users").delete().eq("id", user_id).execute()
    if res.error:
        return jsonify({"error": str(res.error)}), 500
    return jsonify({"deleted": True}), 200
