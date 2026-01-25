from dataclasses import dataclass
import ollama
from typing import List, Dict, Any, Protocol
from logger_config import log
from txt_logger import setup_txt_logger
from pathlib import Path

# Setup json logger
log_file_path = Path(__file__).parent / "ollama-client-log.txt"
txt_logger = setup_txt_logger(__name__, log_file_path)

# model's parameters constants
TEMPERATURE = 0.2
TOP_P = 0.9
# TOP_K = 40
# REPEAT_PENALTY = 1.1

class LLMClient(Protocol):
    def chat(self, model_name: str, messages: List[Dict[str, Any]]) -> str: ...


class OllamaConnectionError(Exception):
    pass


class OllamaClient(LLMClient):

    _client: ollama.Client | None
    options: Dict[str, float] | None

    def __init__(self) -> None:
        self._client: ollama.Client = None
        self.options = {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            # "top_k": TOP_K,
            # "repeat_penalty": REPEAT_PENALTY,
        }

    def connect_to_host(self, host_url: str) -> "OllamaClient":
        try:
            self._client = ollama.Client(host=host_url)
            log.info(f"Cliente Ollama conectado com sucesso ao host: {host_url}")
            txt_logger.info({"variable": "connection_status", "value": f"Successfully connected to {host_url}"})
            return self
        except Exception as e:
            error_message = f"Não foi possível conectar ao servidor Ollama em {host_url}. Detalhes: {e}"
            log.error(error_message)
            txt_logger.info({"variable": "connection_status", "value": error_message})
            raise OllamaConnectionError(error_message) from e

    def create_model(self, base_model: str, model_name: str, system_role: str) -> None:
        try:
            # modelfile = f"FROM {base_model}\nSYSTEM {system_role}"
            self._client.create(model=model_name, from_=base_model, system=system_role)
            success_message = f"Modelo personalizado '{model_name}' criado com sucesso a partir do modelo base '{base_model}'."
            log.info(success_message)
            txt_logger.info({"variable": "model_creation_status", "value": success_message})
        except Exception as e:
            error_message = f"Erro ao criar o modelo personalizado '{model_name}': {e}"
            log.error(error_message)
            txt_logger.info({"variable": "model_creation_status", "value": error_message})

    def list_models(self) -> str:
        try:
            response = self._client.list()
            if response:
                formatted_output: str = "Resposta completa da API:\n"

                # Exibir modelos de forma mais legível
                for model in response["models"]:
                    # Acessando os atributos corretamente do objeto Model
                    model_name = model.model
                    model_size = model.size

                    # Formatando o tamanho para uma representação mais legível
                    size_gb = model_size / (1024**3)  # Converter bytes para GB

                    formatted_output += f"{model_name}\n"
                    formatted_output += f"Tamanho: {size_gb:.2f} GB\n"
                    formatted_output += "\n"

            return formatted_output

        except Exception as e:
            log.error(f"Erro ao listar os modelos: {e}")
            return ""

    def chat(
        self,
        model_name: str,
        messages: List[Dict[str, Any]],
        options: Dict[str, float] | None = None,
    ) -> str:
        if options is None:
            options = self.options
        try:
            log.info(f"Enviando prompt para o modelo '{model_name}'...")
            txt_logger.info({"variable": "chat_status", "value": f"Sending prompt to model '{model_name}'..."})
            response = self._client.chat(
                model=model_name, messages=messages, options=options
            )
            content = response.get("message", {}).get("content", "")
            log.info("Resposta recebida do modelo.")
            txt_logger.info({"variable": "chat_status", "value": "Response received from model."})
            return content
        except Exception as e:
            error_message = f"Erro durante o chat com o modelo '{model_name}': {e}"
            log.error(error_message)
            txt_logger.info({"variable": "chat_status", "value": error_message})
            return ""


if __name__ == "__main__":
    pass
