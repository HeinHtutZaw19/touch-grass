from supabase import create_client

supabase_client = None

def init_app(app):
    global supabase_client
    supabase_client = create_client(app.config["SUPABASE_URL"], app.config["SUPABASE_KEY"])
    app.supabase_client = supabase_client
