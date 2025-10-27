import base64
from pathlib import Path
from typing import List
from openai import OpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv


class GPTChoice(TypedDict):
    message: dict


class GPTResponse(TypedDict):
    choices: List[GPTChoice]


def get_openai_client() -> OpenAI:
    load_dotenv()
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")
    return OpenAI(api_key=api_key)


def gpt_query(client, system_prompt: str, image_path: Path, model: str) -> str:
    # Abrir a imagem e converter para base64
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Enviar para a API
    gpt_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all readable text from this image.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_base64}",
                    },
                ],
            },
        ],
    )

    return gpt_response.choices[0].message["content"]


def extract_text_from_images(
    client: OpenAI, image_paths: List[Path], system_prompt: str, model: str
) -> str:
    """Itera sobre imagens salvas no disco e extrai texto de cada uma."""
    full_text: str = ""
    for img_path in image_paths:
        print(f"Processando imagem: {img_path.name}")
        page_text = gpt_query(client, system_prompt, img_path, model)
        full_text += page_text + "\n\n"
    return full_text.strip()
