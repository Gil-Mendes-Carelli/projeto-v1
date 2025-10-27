import os
import time
from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI
import pymupdf
from PIL import Image
import base64
from io import BytesIO

def get_openai_client() -> OpenAI:
    """Carrega a chave de API e retorna um cliente OpenAI."""
    load_dotenv()
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada.")
    return OpenAI(api_key=api_key)

def convert_pdf_to_images(pdf_path: Path) -> list[Image.Image]:
    """Converte cada página de um PDF em uma imagem PIL."""
    try:
        pdf_document = pymupdf.open(pdf_path)
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        return images
    except Exception as e:
        print(f"Erro ao converter PDF para imagens: {e}")
        return []

def transcribe_image_with_gpt4o(client: OpenAI, image: Image.Image) -> str:
    """Usa a API do GPT-4o para transcrever texto manuscrito em uma imagem."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Transcreva o texto manuscrito contido nesta imagem.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao transcrever imagem com GPT-4o: {e}")
        return ""

def main() -> None:
    """Executa o processo completo de OCR e resposta."""
    pdf_path = Path(r"C:\Users\gilca\Desktop\projeto-v1\chatGPT-ocr\essays\Desafio para valorizacao de comunidades/Giovana Paulino.pdf")
    
    client = get_openai_client()
    assistant_id = None
    vector_store_id = None
    text_file_path = "manuscript_transcription.txt"

    try:
        # 1. Convertendo PDF para imagens
        print("Convertendo PDF para imagens...")
        images = convert_pdf_to_images(pdf_path)
        if not images:
            print("Nenhuma imagem extraída. Abortando.")
            return
        
        # 2. Transcrevendo imagens com GPT-4o
        transcribed_text = ""
        print("Iniciando a transcrição do texto manuscrito...")
        for i, img in enumerate(images):
            print(f"Transcrevendo página {i + 1}...")
            transcribed_text += f"\n--- Página {i + 1} ---\n"
            transcribed_text += transcribe_image_with_gpt4o(client, img)
        
        # 3. Salvando o texto transcrito em um arquivo temporário
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        print(f"Transcrição salva em '{text_file_path}'")

        # 4. Upload do arquivo de texto e criação do vector store
        file = client.files.create(
            file=open(text_file_path, "rb"),
            purpose='assistants'
        )
        print(f"Arquivo de texto criado com ID: {file.id}")
        
        vector_store = client.vector_stores.create(
            name="Manuscrito Vector Store",
            file_ids=[file.id]
        )
        vector_store_id = vector_store.id
        print(f"Vector Store criado com ID: {vector_store_id}")

        # 5. Criar assistente e thread
        assistant = client.beta.assistants.create(
            name="Assistente de Manuscrito",
            instructions="""
                You are an OCR transcription assistant specialized in accurately converting handwritten text from PDF documents into digital text.

                Your main objective is to transcribe the text exactly as it appears in the original document, without correcting or interpreting any errors. 
                The document is written in Portuguese (Brazilian). You must preserve the original language — do not translate, correct, or modify the text.

                Maintain all original spelling mistakes, grammatical issues, punctuation, capitalization, and line breaks.
                If a word or section is unreadable, write [ilegível] in its place (use Portuguese for this placeholder).

                Guidelines:
                - Keep the same paragraph and line structure as the handwritten document.
                - Do not add explanations, comments, or notes.
                - Output only the transcribed text, nothing else.
                """,
            tools=[{"type": "file_search"}],
            model="gpt-4o",
            tool_resources={
                "file_search": {"vector_store_ids": [vector_store_id]}
            }
        )
        assistant_id = assistant.id
        print(f"Assistente criado com ID: {assistant_id}")

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Extract the text from the pdf file",
                }
            ]
        )
        print(f"Thread criada com ID: {thread.id}")

        # 6. Executar e obter a resposta
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = next(
            (m for m in messages.data if m.role == "assistant"), None
        )

        if assistant_message:
            print("\nResposta do Assistente:")
            for content in assistant_message.content:
                if content.type == "text":
                    print(content.text.value)

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")

    finally:
        print("\nIniciando a limpeza dos recursos...")
        if assistant_id:
            try:
                client.beta.assistants.delete(assistant_id)
                print("Assistente excluído com sucesso.")
            except Exception as e:
                print(f"Erro ao excluir o assistente: {e}")

        if vector_store_id:
            try:
                client.vector_stores.delete(vector_store_id)
                print("Vector Store excluído com sucesso.")
            except Exception as e:
                print(f"Erro ao excluir o vector store: {e}")
        
        if os.path.exists(text_file_path):
            os.remove(text_file_path)
            print(f"Arquivo temporário '{text_file_path}' excluído.")

if __name__ == "__main__":
    main()
