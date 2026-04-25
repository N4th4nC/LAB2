from supabase import create_client

SUPABASE_URL = "SUA_URL"
SUPABASE_KEY = "SUA_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
