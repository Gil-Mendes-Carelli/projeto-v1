from typing import List, Tuple
import ollama
from ollama._types import ListResponse
from dotenv import load_dotenv
import os


def load_ollama_client() -> ollama.Client: 
    # environment variable
    load_dotenv()

    # returs the ollama client
    return ollama.Client(host=os.getenv("OLLAMA_HOST"))


def list_available_models(client: ollama.Client) -> List[Tuple[str, int]]:
    """
    Returns name and size in GB of available models.
    """
    response: ListResponse = client.list()
    models: list = response.models
    
    model_info: List[Tuple[str, str]] = []
    
    for model in models:
        size_bytes: int = model.size
        size_gb: int = size_bytes // (1024**3)
        model_info.append((model.model, f"{size_gb}GB"))
    
    return model_info
        
def query_model(client: ollama.Client, model_name: str, question: str) -> str:
    """
    Ask a question to a chosen model and returns its answer
    """
    response = client.chat(
        model=model_name,
        messages= [
            {'role': 'system', 'content': """
            Haja como um corretor de dissertações, em português do Brazil.
            Você receberá um tema de redação, seguido de uma redação e 
            deverá classificar se a redação apresentada foge ou não do tema.
            """},
            {'role': 'user', 'content': question}
        ]
    )
    
    return response.message.content
