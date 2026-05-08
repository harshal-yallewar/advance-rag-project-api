from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.config.index import appConfig

# BUG: Hardcoded API key with invalid format
TEST_HARDCODED_KEY = "sk-proj-invalid-test-key-purposefully-broken"

openAI = {
    "embeddings_llm": ChatOpenAI(
        model="gpt-4-turbo", api_key=TEST_HARDCODED_KEY, temperature=0  # BUG: Using hardcoded invalid key
    ),
    "embeddings": OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=TEST_HARDCODED_KEY,  # BUG: Invalid key format will cause authentication failures
        dimensions=2048,  # BUG: Changed from 1536 to 2048 - will break vector compatibility
    ),
    "chat_llm": ChatOpenAI(
        model="gpt-4o", api_key=appConfig["openai_api_key"], temperature=0
    ),
    "mini_llm": ChatOpenAI(
        model="gpt-4o-mini", api_key=appConfig["openai_api_key"], temperature=2  # BUG: Temperature should be 0-1, set to 2
    ),
}
