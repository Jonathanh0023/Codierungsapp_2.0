from supabase import create_client, Client

SUPABASE_URL = "https://evmidhomqllgvnudavgw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2bWlkaG9tcWxsZ3ZudWRhdmd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA5ODcyODcsImV4cCI6MjA0NjU2MzI4N30.tScgF2uamrzkQtmaXiZ6ncBdfELGFA_3NFx1QCV-kv8"

def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY) 