from flask import Blueprint, jsonify, current_app as app
from datetime import datetime
import random
import re
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os
import json

recommend_bp = Blueprint("recommend", __name__)
VALID_CATEGORIES = {"analytical","creative","social","physical"}

import re

def _is_similar(a: str, b: str) -> bool:
    if not a or not b:
        return False
    na = re.sub(r'\s+',' ', a.strip().lower())
    nb = re.sub(r'\s+',' ', b.strip().lower())
    return na == nb or na in nb or nb in na

def _get_datamap(user_id):
    try:
        dm = app.supabase_client.table("datamaps").select("*").eq("user_id", user_id).single().execute()
        if dm.data:
            return dm.data
        return {}
    except Exception as e:
        print("datamap select error: %s", e)

def _dominant_category(prefs: dict):
    if not prefs:
        return None
    filtered = {k: float(v or 0) for k,v in prefs.items() if k in VALID_CATEGORIES}
    if not filtered:
        return None
    if all(v == 0 for v in filtered.values()):
        return random.choice(list(prefs))
    maxv = max(filtered.values())
    ties = [k for k,v in filtered.items() if v == maxv]
    return random.choice(ties)

def _pick_hobby(category):
    try:
        res = app.supabase_client.table("hobbies").select("*").eq("category", category).execute()
        if not res.data:
            return None
        return random.choice(res.data)
    except Exception as e:
        print("hobby select error: %s", e)
        return None

def _pick_unused_fun_fact(hobbies_id, user_id):
    # fetch facts for hobby
    facts_res = app.supabase_client.table("fun_facts").select("*").eq("hobbies_id", hobbies_id).execute()
    facts = facts_res.data if facts_res and facts_res.data else []
    if not facts:
        return None, None

    # filter facts that user has seen: check ai_interactions.fun_fact (fact id)
    unseen = []
    for f in facts:
        seen_res = app.supabase_client.table("ai_interactions").select("*") \
            .eq("user_id", user_id).eq("fun_fact_id", f["id"]).limit(1).execute()
        seen = seen_res.data and len(seen_res.data)>0
        if not seen:
            unseen.append(f)

    if unseen:
        chosen = random.choice(unseen)
        return chosen["id"], chosen["text"]
    # if all seen, return None
    return None, None

import asyncio
import os
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from datetime import datetime

load_dotenv()

# OpenAI model
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Firecrawl server
server_params = StdioServerParameters(
    command="npx",
    env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
    args=["firecrawl-mcp"]
)

async def generate_hobby_and_fact(category, avoid, user_context):
    """
    Use Agentic + Firecrawl to fetch one hobby + fun fact dynamically.
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            # system prompt tells Agentic to crawl only one page
            system_msg = {
                "role": "system",
                "content": (
                    "You are a friendly, kid-focused Hobby Recommendation AI. "
                    f"For the category '{category}', choose exactly ONE hobby aside from {avoid} that is appropriate for kids. \n\n"

                    "Return a JSON object with the following fields:\n"
                    " - name: The name of the hobby.\n"
                    " - fun_fact: A short, playful fun fact that would excite a child.\n"
                    " - description: A small, creative activity that a kid can try RIGHT NOW with. "
                    "The activity must directly relate to the chosen hobby and must sound fun, imaginative, and encouraging. "
                    "End the description with a suggestion for ONE photo the child can take related to their creation. The kid must take a photo to this creation\n\n"

                    "Tone rules:\n"
                    " - Use positive, cheerful wording.\n"
                    " - Be simple and clear.\n"
                    " - Avoid adult vocabulary.\n"
                    " - Encourage curiosity.\n\n"

                    "STRICT RULES:\n"
                    " - Output must be ONLY valid JSON.\n"
                    " - No extra sentences before or after.\n"
                    " - No markdown.\n"
                    " - No backticks.\n"
                    " - Do not invent false facts.\n"
                    " - The description must be specifically about the hobby, not something random.\n\n"

                    "Format to return exactly:\n"
                    "{\"name\": ..., \"fun_fact\": ..., \"description\": ...}"
                )
            }

            # optionally include user context
            user_prompt = {
                "role": "user",
                "content": f"User context: {user_context}"
            }

            # invoke the agent
            try:
                response = await agent.ainvoke({"messages": [system_msg, user_prompt]})
                # last message from agent
                ai_message = response["messages"][-1].content
                return ai_message  # should be JSON string with name, fun_fact, description
            except Exception as e:
                print("Agentic crawl error:", e)
                # fallback
                FALLBACK = {
                    "analytical": ("Logic Puzzles", "Logic puzzles train your deduction and planning skills.", ""),
                    "creative": ("Sketch Journaling", "Sketch journaling helps capture daily creativity.", ""),
                    "social": ("Board Game Night", "Board games are great low-pressure social practice.", ""),
                    "physical": ("Parkour Basics", "Parkour increases agility and spatial awareness.", "")
                }
                name, fact, desc = FALLBACK.get(category, ("Try Something New", f"Explore {category} activities.", ""))
                return {"name": name, "fun_fact": fact, "description": desc}


@recommend_bp.route("/", methods=["GET"])
def hello():
    return "HELLO"
@recommend_bp.route("/<user_id>", methods=["GET"])
def recommend(user_id):
    # 1) get datamap
    prefs = _get_datamap(user_id)

    # 2) pick hobby
    dominant = _dominant_category(prefs)

    chosen_fact_id = None
    chosen_fact_text = None
    try:
        hobby_names = app.supabase_client.table("hobbies").select("name").eq("category", dominant).execute()

        gen = asyncio.run(generate_hobby_and_fact(dominant, hobby_names, {"user_id": user_id, "prefs": prefs}))
        gen = json.loads(gen.strip())
        create_h = app.supabase_client.table("hobbies").insert({
            "name": gen["name"],
            "category": dominant,
            "description": gen.get("description")
        }).execute()
        if not create_h or not create_h.data:
            print("Failed to create hobby")
            hobby = {"id": None, "name": gen["name"], "description": gen.get("description")}
        else:
            hobby = create_h.data[0]
             # insert fun_fact and link to hobby
            try:
                ins = app.supabase_client.table("fun_facts").insert({
                    "hobbies_id": hobby.get("id"),
                    "text": gen["fun_fact"],
                    "created_at": datetime.utcnow().isoformat()
                }).execute()
                if ins.data and len(ins.data)>0:
                    chosen_fact_id = ins.data[0]["id"]
                    chosen_fact_text = ins.data[0]["text"]
                else:
                    chosen_fact_text = gen["fun_fact"]
            except Exception as e:
                print("insert fun_fact failed: %s", e)
                chosen_fact_text = gen["fun_fact"]
                log_payload = {
                    "user_id": user_id,
                    "prompt": f"Recommendation for category {dominant}",
                    "fun_fact_id": chosen_fact_id,
                    "category": dominant,
                    "created_at": datetime.utcnow().isoformat()
                }
                app.supabase_client.table("ai_interactions").insert(log_payload).execute()
                return jsonify({
                    "user_id": user_id,
                    "dominant_category": dominant,
                    "hobby": {"id": hobby.get("id"), "name": hobby.get("name"), "description": hobby.get("description")},
                    "fun_fact_id": chosen_fact_id,
                    "fun_fact_text": chosen_fact_text
                }), 200
    except Exception as e:
        print("create hobby failed: %s", e)

