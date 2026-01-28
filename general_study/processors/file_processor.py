#####################################################################################################
############## This file processor is design to work with default installation models ###############
#####################################################################################################
################# It's main function is to process a text from a file through a LLM #################
#####################################################################################################
import os
from pathlib import Path
from dataclasses import dataclass

from host.llm_host import HostClient
from logger.txt_logger import setup_txt_logger
from helper_functions.helper_functions import load_text_from_file

# Setup logger
log_file_path = Path(__file__).parent / "file-proc-log.txt"
txt_logger = setup_txt_logger(__name__, log_file_path)


@dataclass(slots=True)
class ProcessFilesConfig:
    file_path: Path
    model_name: str
    client: HostClient
    system_role: str | None


def process_files(config: ProcessFilesConfig) -> str:
    """
    Process files using a LLM.

    Args:
        A ProcessFilesConfig objet with all configurations.
    """
    txt_logger.info({"variable": "model name", "value": config.model_name})

    if config.file_path.exists() and config.file_path.isfile():
        ignored_file = os.getenv("IGNORED_FILE_NAME")
        if config.file_path.name != ignored_file:
            file_text: str = load_text_from_file(config.file_path)
            messages: list[dict[str, str]] = []
            messages.append({"role": "system", "content": config.system_role or ""})
            messages.append({"role": "user", "content": file_text})

            txt_logger.info(
                {"variable": "config.system_role", "value": config.system_role}
            )
            txt_logger.info({"variable": "text", "value": file_text})

            response: str = config.client.chat(
                model_name=config.model_name,
                messages=messages,
                options=config.client.options,
            )

            txt_logger.info({"variable": "response", "value": response})

            return response

        return ""

    raise FileNotFoundError(f"File not found: {config.file_path}")


def main() -> None:
    pass


if __name__ == "__main__":
    main()

    # if config.output_file_name:
    #     save_response_to_file(
    #         response, config.file_path.name, config.output_file_name
    #     )
    # else:
    #     raise ValueError("Output file name is not valid.")
