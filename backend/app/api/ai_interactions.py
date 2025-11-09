from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime

ai_interactions_bp = Blueprint("ai_interactions", __name__)

VALID_CATEGORIES = {"analytical", "creative", "social", "physical"}
ALPHA = 0.2  # weight for new feedback in EMA update (0 < ALPHA <= 1)

def _ensure_datamap(user_id):
    """Return datamap row; create if missing."""
    try:
        dm = app.supabase_client.table("datamaps").select("*").eq("user_id", user_id).single().execute()
        if dm.data:
            return dm.data
        try:
            create = app.supabase_client.table("datamaps").insert({
                "user_id": user_id,
                "analytical": 0,
                "creative": 0,
                "social": 0,
                "physical": 0
            }).select("*").execute()
            return create.data[0]
        except Exception as e:
            print("Failed to create datamap for user %s: %s", user_id, e)
            return None
    except Exception as e:
        print("datamap select error: %s", e)

def _update_datamap_category(user_id, category, feedback):
    """Update only the given category using EMA: new = old*(1-alpha) + feedback*alpha"""
    if category not in VALID_CATEGORIES:
        raise ValueError("invalid category")

    dm = _ensure_datamap(user_id)
    if dm is None:
        return None

    old_value = float(dm.get(category) or 0)
    new_value = round(old_value * (1 - ALPHA) + float(feedback) * ALPHA, 4)
    try:
        upd = app.supabase_client.table("datamaps").update({
            category: new_value
        }).eq("user_id", user_id).select("*").execute()
    except Exception as e:
        print("Failed to update datamap for user %s: %s", user_id, e)
        return None
    return upd.data[0]

@ai_interactions_bp.route("/", methods=["GET"])
def list_interactions():
    user_id = request.args.get("user_id")
    q = app.supabase_client.table("ai_interactions").select("*")
    if user_id:
        q = q.eq("user_id", user_id)
    try:
        res = q.execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@ai_interactions_bp.route("/", methods=["POST"])
def create_interaction():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    category = data.get("category")
    feedback = data.get("user_feedback")  # integer 1..5

    if not user_id or not category:
        return jsonify({"error": "user_id and category are required"}), 400
    if category not in VALID_CATEGORIES:
        return jsonify({"error": f"category must be one of {sorted(VALID_CATEGORIES)}"}), 400
    if feedback is not None:
        try:
            feedback = int(feedback)
            if not (1 <= feedback <= 5):
                raise ValueError()
        except Exception:
            return jsonify({"error": "user_feedback must be integer 1..5"}), 400

    # optional fields
    payload = {
        "user_id": user_id,
        "prompt": data.get("prompt") or "",
        "fun_fact_id": data.get("fun_fact_id"),
        "category": category,
        "user_feedback": feedback,
        "response": data.get("response"),
        "media_url": data.get("media_url"),
        "created_at": datetime.utcnow().isoformat()
    }

    # 1) Insert the interaction
    ins = app.supabase_client.table("ai_interactions").insert(payload).select("*").execute()
    if ins.error:
        return jsonify({"error": str(ins.error)}), 500
    created = ins.data[0]

    # 2) If feedback present, update only the relevant category
    updated_datamap = None
    if feedback is not None:
        updated_datamap = _update_datamap_category(user_id, category, feedback)

    result = {"interaction": created}
    if updated_datamap:
        result["datamap"] = updated_datamap

    return jsonify(result), 201

@ai_interactions_bp.route("/<interaction_id>", methods=["GET"])
def get_interaction(interaction_id):
    try:
        res = app.supabase_client.table("ai_interactions").select("*").eq("id", interaction_id).single().execute()
        if not res.data:
            return jsonify({"error": "Interaction not found"}), 404
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@ai_interactions_bp.route("/<interaction_id>", methods=["DELETE"])
def delete_interaction(interaction_id):
    try:
        res = app.supabase_client.table("ai_interactions").delete().eq("id", interaction_id).execute()
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": e}), 500
