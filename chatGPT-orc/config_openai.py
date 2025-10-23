from __future__ import annotations
from openai import OpenAI
from dotenv import load_dotenv
import os

def get_openai_client() -> OpenAI:    
    # loading variables
    load_dotenv()
    # loading api key
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")
    # loading the client
    client = OpenAI(api_key=api_key)      

    return client
