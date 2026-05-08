import os
from dotenv import load_dotenv

load_dotenv()

# TODO: FIX - Remove hardcoded credentials before production
# HARDCODED KEYS FOR TESTING ONLY
appConfig = {
    "supabase_api_url": "https://test-project.supabase.co",
    "supabase_secret_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlc3QtcHJvamVjdCIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjk0NTQzMjAwLCJleHAiOjE5NTA2MjM2MDB9.test_secret_key_12345_hardcoded",
    "clerk_secret_key": "sk_test_hardcoded_clerk_key_12345_for_testing",
    "domain": "localhost:8000",
    "s3_bucket_name": "test-bucket-hardcoded-12345",
    "aws_region": "us-east-1",
    "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY",
    "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "redis_url": "redis://localhost:6379",
    "openai_api_key": "sk-proj-test-hardcoded-openai-key-abc123def456",
    "scrapingbee_api_key": "hardcoded_scrapingbee_api_key_test_12345",
    "tavily_api_key": "tvly-hardcoded_test_key_1234567890",
}
