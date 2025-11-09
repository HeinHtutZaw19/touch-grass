from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime

fun_facts_bp = Blueprint("fun_facts", __name__)

@fun_facts_bp.route("/", methods=["GET"])
def list_fun_facts():
    # optionally filter by hobbies_id
    hobbies_id = request.args.get("hobbies_id")
    q = app.supabase_client.table("fun_facts").select("*")
    if hobbies_id:
        q = q.eq("hobbies_id", hobbies_id)
    try:
        res = q.execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@fun_facts_bp.route("/", methods=["POST"])
def create_fun_fact():
    data = request.get_json() or {}
    hobbies_id = data.get("hobbies_id")
    text = data.get("text")
    if not hobbies_id or not text:
        return jsonify({"error":"hobbies_id and text required"}), 400

    payload = {
        "hobbies_id": hobbies_id,
        "text": text,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        res = app.supabase_client.table("fun_facts").insert(payload).select("*").execute()
        return jsonify(res.data[0]), 201
    except Exception as e:
        return jsonify({"error": e}), 500

@fun_facts_bp.route("/<fact_id>", methods=["GET"])
def get_fun_fact(fact_id):
    try:
        res = app.supabase_client.table("fun_facts").select("*").eq("id", fact_id).single().execute()
        if not res.data:
            return jsonify({"error":"Fun fact not found"}), 404
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@fun_facts_bp.route("/<fact_id>", methods=["DELETE"])
def delete_fun_fact(fact_id):
    try:
        res = app.supabase_client.table("fun_facts").delete().eq("id", fact_id).execute()
        return jsonify({"deleted": True}), 200
    except Exception as e:
        return jsonify({"error": e}), 500
