# Projeto para estudo sobre as capacidade de LLMs open-source

Este projeto foi criado em Python para explorar e interagir com modelos de linguagem de grande porte (LLMs) open-source através de um servidor Ollama. Ele fornece um cliente para se conectar ao host do Ollama, listar modelos, criar modelos personalizados e iniciar sessões de chat.

A aplicação está sendo desenvolvida com uma interface gráfica usando PySide6.

## Core Features

-   **Ollama Client**: Um cliente robusto para interagir com a API do Ollama.
-   **Host Connection**: Conecta-se a uma instância do servidor Ollama em execução.
-   **Model Management**: Lista os modelos disponíveis no host.
-   **Chat Interaction**: Envia prompts e recebe respostas de qualquer modelo selecionado.
-   **Logging**: Configuração de logger centralizado para rastreamento de eventos e depuração.

## Getting Started

### Prerequisites

-   Python 3.11+
-   `pip` e `pip-tools`
-   Uma instância do [Ollama](https://ollama.com/) em execução.

### Installation

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Gil-Mendes-Carelli/projeto-v1.git
    cd projeto-v1
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O projeto usa `pip-tools` para gerenciamento de dependências. Os pacotes necessários estão listados em `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Usage Example

Você pode usar o `OllamaClient` para interagir com seu servidor Ollama. Aqui está um exemplo básico de como usá-lo em um script Python:

```python
from llm_host.ollama_client import OllamaClient, OllamaConnectionError

# Substitua pela URL do seu host Ollama
OLLAMA_HOST = "http://localhost:11434"

try:
    # 1. Conecte-se ao servidor Ollama
    client = OllamaClient().connect_to_host(OLLAMA_HOST)

    # 2. Liste os modelos disponíveis
    models_list = client.list_models()
    print("Modelos disponíveis:")
    print(models_list)

    # 3. Inicie um chat com um modelo (ex: llama3)
    # Certifique-se de ter o modelo baixado: `ollama pull llama3`
    model_name = "llama3"
    prompt = "Explique a computação quântica em termos simples."

    print(f"\nEnviando prompt para o modelo '{model_name}'...")
    response = client.chat(model_name, prompt)

    print("\nResposta do modelo:")
    print(response)

except OllamaConnectionError as e:
    print(f"Erro de conexão: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
```

## Project Structure

```
├── llm-host/
│   └── ollama_client.py  # Cliente principal para interagir com a API do Ollama
├── logger_config.py      # Configuração centralizada do logger
├── requirements.in       # Definição das dependências do projeto
├── requirements.txt      # Lista de pacotes congelados para instalação
└── ...
```

## 🗺️ Roadmap / To-Do

-   [ ] Configurar interface gráfica inicial com **PySide6**
-   [ ] Definir arquitetura do projeto (módulos, pacotes, pastas)
-   [ ] Criar tela principal da aplicação
-   [ ] Adicionar testes unitários
-   [ ] Preparar documentação mais detalhada
-   [ ] Criar sistema de releases no GitHub
