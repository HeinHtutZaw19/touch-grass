import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", True)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

