import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")
    return OpenAI(api_key=api_key)
