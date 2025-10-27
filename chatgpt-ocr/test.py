import os
from pathlib import Path
from dotenv import load_dotenv

from openai import OpenAI


def get_openai_client() -> OpenAI:
    load_dotenv()
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")
    return OpenAI(api_key=api_key)


def main() -> None:
    
    pdf_path = Path(r"C:\Users\gilca\Desktop\projeto-v1\chatGPT-ocr\essays\Desafio para valorizacao de comunidades/Giovana Paulino.pdf")
    
    client = get_openai_client()

    try:
        # 1. Fazer o upload do arquivo PDF e criar um vetor store simultaneamente
        # O arquivo é automaticamente analisado, dividido e incorporado
        vector_store = client.vector_stores.create(
            name="PDF Assistant Vector Store",
            file_ids=[
                client.files.create(
                    file=open(pdf_path, "rb"),
                    purpose='assistants'
                ).id
            ]
        )
        print(f"Vector Store criado com ID: {vector_store.id}")

        # 2. Criar um assistente para usar a ferramenta de pesquisa de arquivo
        assistant = client.beta.assistants.create(
            name="Assistente de PDF",
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
                "file_search": {"vector_store_ids": [vector_store.id]}
            }
        )
        print(f"Assistente criado com ID: {assistant.id}")

        # 3. Criar um thread (conversa)
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Poderia resumir os principais pontos do documento?",
                }
            ]
        )
        print(f"Thread criada com ID: {thread.id}")

        # 4. Executar o assistente no thread para processar a mensagem
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # 5. Recuperar e imprimir a resposta do assistente
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
        print(f"Ocorreu um erro: {e}")

    finally:
        # 6. Limpeza (opcional): Excluir recursos criados
        print("\nIniciando a limpeza dos recursos...")
        try:
            if 'assistant' in locals():
                client.beta.assistants.delete(assistant.id)
                print("Assistente excluído com sucesso.")
        except Exception as e:
            print(f"Erro ao excluir o assistente: {e}")

        try:
            if 'vector_store' in locals():
                client.vector_stores.delete(vector_store.id)
                print("Vector Store excluído com sucesso.")
        except Exception as e:
            print(f"Erro ao excluir o vector store: {e}")
            
            
if __name__ == "__main__":
    main()
