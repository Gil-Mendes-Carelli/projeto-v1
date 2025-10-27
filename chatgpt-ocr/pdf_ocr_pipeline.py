from pathlib import Path
from typing import List
from pdf_to_images import pdf_to_images
from openai_client import get_openai_client, extract_text_from_images, OpenAI


def validate_pdf_path(pdf_path: Path) -> Path:
    """Valida se o caminho é um PDF existente."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"O caminho informado não é um arquivo PDF válido: {pdf_path}")
    return pdf_path


def save_extracted_text(output_dir: Path, pdf_path: Path, extracted_text: str) -> Path:
    """Salva o texto extraído em arquivo .txt no diretório de saída."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{pdf_path.stem}_extracted.txt"
    output_file.write_text(extracted_text, encoding="utf-8")
    print(f"Texto salvo em: {output_file}")
    return output_file


def process_single_pdf(
    client: OpenAI, pdf_path: Path, output_dir: Path, system_prompt: str, model: str
) -> Path:
    """
    Converte PDF em imagens, salva no disco, envia ao GPT e salva o texto extraído.
    """
    poppler_bin = r"C:\poppler\Library\bin"
    image_paths = pdf_to_images(
        pdf_path, output_dir, poppler_bin
    )  # salva as imagens no disco

    extracted_text = extract_text_from_images(client, image_paths, system_prompt, model)
    return save_extracted_text(output_dir, pdf_path, extracted_text)


def process_pdf_directory(
    pdf_dir: Path, output_dir: Path, system_prompt: str, model: str = "gpt-4o"
) -> List[Path]:
    """Processa todos os PDFs de um diretório."""
    if not pdf_dir.exists() or not pdf_dir.is_dir():
        raise FileNotFoundError(f"Diretório não encontrado: {pdf_dir}")

    client = get_openai_client()
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"Nenhum PDF encontrado no diretório: {pdf_dir}")

    saved_files: List[Path] = []
    for pdf in pdf_files:
        print(f"Processando {pdf.name}...")
        saved_file = process_single_pdf(client, pdf, output_dir, system_prompt, model)
        saved_files.append(saved_file)

    return saved_files


if __name__ == "__main__":
    pass
