from flask import Blueprint, request, jsonify, current_app as app

datamaps_bp = Blueprint("datamaps", __name__)

@datamaps_bp.route("/<user_id>", methods=["GET"])
def get_datamap(user_id):
    try:
        res = app.supabase_client.table("datamaps").select("*").eq("user_id", user_id).single().execute()
        if not res.data:
            return jsonify({"error": "Datamap not found"}), 404
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@datamaps_bp.route("/", methods=["POST"])
def create_datamap():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    payload = {
        "user_id": user_id,
        "analytical": data.get("analytical", 0),
        "creative": data.get("creative", 0),
        "social": data.get("social", 0),
        "physical": data.get("physical", 0)
    }
    try:
        res = app.supabase_client.table("datamaps").insert(payload).select("*").execute()
        return jsonify(res.data[0]), 201
    except Exception as e:
        return jsonify({"error": e}), 500

@datamaps_bp.route("/<user_id>", methods=["PATCH"])
def patch_datamap(user_id):
    data = request.get_json() or {}
    allowed = {"analytical", "creative", "social", "physical"}
    payload = {k: v for k, v in data.items() if k in allowed}
    if not payload:
        return jsonify({"error": "No valid datamap fields provided"}), 400
    try:
        res = app.supabase_client.table("datamaps").update(payload).eq("user_id", user_id).select("*").execute()
        if not res.data:
            return jsonify({"error": "Datamap not found"}), 404
        return jsonify(res.data[0]), 200
    except Exception as e:   
        return jsonify({"error": e}), 500

@datamaps_bp.route("/<user_id>", methods=["DELETE"])
def delete_datamap(user_id):
    try:
        res = app.supabase_client.table("datamaps").delete().eq("user_id", user_id).execute()
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": e}), 500