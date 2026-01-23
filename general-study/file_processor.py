from pathlib import Path
from docx import Document
from dataclasses import dataclass

from ollama_client import LLMClient


@dataclass(slots=True)
class ProcessFilesConfig:
    files_text: list[str]
    model_name: str
    client: LLMClient
    system_role: str | None
    output_file_name: str | None


def process_files(config: ProcessFilesConfig) -> None:
    """
    Process files using a LLM.

    Args:
        A ProcessFilesConfig objet with all configurations.
    """

    # Iteration over read texts from the files
    for text in config.files_text:
        # Inserting system role message
        messages: list[dict[str, str]] = []
        messages.append({"role": "system", "content": config.system_role or ""})
        messages.append({"role": "user", "content": text})
        # Chatting with a model
        response = config.client.chat(
            model_name=config.model_name,
            messages=messages,
            options=config.client.options,
        )

        # Saving model's response to a file
        if config.output_file_name:
            save_response_to_file(response, config.output_file_name)
        else:
            raise ValueError("Output file name is not valid.")


##### Helpers functions #####
def load_file_texts_from_folder(folder: Path) -> list[str]:
    texts: list[str] = []

    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() == ".docx":
            document: Document = Document(path)
            content: str = "\n".join(
                paragraph.text for paragraph in document.paragraphs
            )
            texts.append(content)

    return texts


def save_response_to_file(
    response: str, output_file: Path = Path("classification_results.txt")
) -> None:
    output_file = Path.cwd() / output_file
    with output_file.open("a", encoding="utf-8") as f:
        f.write(response + "\n")


##### End of helpers functions #####


def main() -> None:
    pass


if __name__ == "__main__":
    main()
