from supabase import Client, create_client
from src.config.index import appConfig

# HARDCODED SUPABASE CREDENTIALS FOR TESTING
HARDCODED_SUPABASE_URL = "https://hardcoded-test.supabase.co"
HARDCODED_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.hardcoded_test_key_only"

# BUG: Using hardcoded credentials instead of config
supabase: Client = create_client(
    HARDCODED_SUPABASE_URL, HARDCODED_SUPABASE_KEY  # BUG: Hardcoded credentials will not work in production
)
