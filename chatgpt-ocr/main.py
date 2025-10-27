# main.py

from pathlib import Path
from pdf_ocr_pipeline import process_pdf_directory

SYSTEM_PROMPT = """
You are an OCR transcription assistant specialized in accurately converting handwritten text from PDF documents into digital text.

Your main objective is to transcribe the text exactly as it appears in the original document, without correcting or interpreting any errors. 
The document is written in Portuguese (Brazilian). You must preserve the original language — do not translate, correct, or modify the text.

Maintain all original spelling mistakes, grammatical issues, punctuation, capitalization, and line breaks.
If a word or section is unreadable, write [ilegível] in its place (use Portuguese for this placeholder).

Guidelines:
- Keep the same paragraph and line structure as the handwritten document.
- Do not add explanations, comments, or notes.
- Output only the transcribed text, nothing else.
"""

def main():
    pdf_dir = Path(r"C:\Users\gilca\Desktop\projeto-v1\chatGPT-ocr\essays\Desafio para valorizacao de comunidades")
    output_dir = pdf_dir / "resultados"

    print(f"Procurando PDFs em: {pdf_dir}")
    print(f"Resultados serão salvos em: {output_dir}")

    saved_files = process_pdf_directory(pdf_dir, output_dir, SYSTEM_PROMPT, model="gpt-4o")
    print(f"\nTodos os PDFs processados. Arquivos gerados: {len(saved_files)}")

if __name__ == "__main__":
    main()
