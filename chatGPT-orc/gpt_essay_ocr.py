import os
import re
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv

# loading variables
load_dotenv()
# loading api key
api_key: str | None = os.getenv("OPENAI_API_KEY")
# loading the client
client = OpenAI(api_key=api_key)
