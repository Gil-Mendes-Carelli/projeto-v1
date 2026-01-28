**# LLM Document Processor**

**  

A flexible and extensible Python framework for processing text documents using Large Language Models (LLMs). Built with modularity and configurability in mind, this project enables automated analysis, classification, and processing of `.docx` (at this moment) files through customizable LLM interactions.

  

## 🎯 Overview

  

This project provides a robust foundation for document processing workflows powered by LLMs. It features configurable system prompts, comprehensive logging, and a clean architecture that separates concerns for easy extension and maintenance.

  

### Core Capabilities

  

- **Document Processing**: Automated extraction and processing of `.docx` files

- **Flexible LLM Integration**: Support for various LLM providers (currently Ollama)

- **Customizable System Roles**: Define custom behaviors and contexts for different use cases

- **Smart Text Extraction**: Automatic section detection (stops at double blank lines)

- **Comprehensive Logging**: Detailed text-based logging of inputs, outputs, and operations

- **Environment-Based Configuration**: Secure credential and settings management via `.env`

  

## 🚀 Use Cases

  

The architecture supports a wide range of applications:

  

### Current Implementation

- Essay/document analysis and classification

- Automated feedback generation

- Content evaluation with custom criteria

  

### Potential Extensions

- **Educational**: Automated grading, feedback generation, plagiarism detection

- **Legal**: Contract analysis, clause extraction, compliance checking

- **Business**: Email classification, report summarization, sentiment analysis

- **Content**: Article summarization, fact-checking, bias detection

- **Customer Service**: Ticket classification, response suggestion, sentiment tracking

  

## 📋 Requirements

  

- Python 3.11+

- Ollama server (or compatible LLM host)

- `.docx` file support via `python-docx`

  

## 🛠️ Installation

  

1. Clone the repository:

```bash

git clone <repository-url>

cd <project-directory>

```

  

2. Create and activate a virtual environment:

```bash

python -m venv .venv

source .venv/bin/activate  # Linux/Mac

# or

.venvScriptsactivate  # Windows

```

  

3. Install required packages:

```bash

pip install -r requirements.txt

```

  

4. Configure environment variables:

  

Create a `.env` file in the project root:

```env

OLLAMA_HOST=http://localhost:11434

IGNORED_FILE_NAME=TEMA.docx

```

  

5. Install the project in editable mode (for development):

```bash

cd general_study  # or your study directory

pip install -e .

```

  

## 💻 Usage

  

### Basic Document Processing

```python

from pathlib import Path

from processors import file_processor_v2

from host.ollama_client import OllamaClient

import os

  

# Initialize client

client = OllamaClient()

client.connect_to_host(host_url=os.getenv("OLLAMA_HOST"))

  

# Load system role/instructions

system_role = file_processor_v2.load_system_role_from_file(

    Path("path/to/instructions.txt")

)

  

# Configure processing

config = file_processor_v2.ProcessFilesConfig(

    file_path=Path("path/to/document.docx"),

    model_name="llama3.1:latest",

    client=client,

    system_role=system_role

)

  

# Process document

response = file_processor_v2.process_files(config)

print(response)

```

  

### Model Configuration

  

The system supports any Ollama-compatible model. Popular options:

- `llama3.1:latest`

- `gemma:latest`

- `mistral:latest`

- Custom fine-tuned models

  

## 📊 Logging

  

All operations are logged to text files for debugging and auditing:

- Input documents and extracted text

- System roles and configurations

- Model responses

- Timestamps and metadata

  

Log files are stored alongside processing scripts (e.g., `file-proc-log.txt`).

  

## 🔐 Security Notes

  

- Never commit `.env` files to version control

- Keep API keys and host URLs in environment variables

- Review logs before sharing as they contain processed content

  

## 🧪 Development

  

### Running Tests

```bash

# TODO: Add testing framework

```

  

### Code Style

- Type hints throughout

- Dataclasses for configuration

- Modular, single-responsibility functions

- Comprehensive docstrings

  

## 🛣️ Roadmap

  

- [ ] Batch processing with parallel execution

- [ ] Support for multiple LLM providers (OpenAI, Anthropic, etc.)

- [ ] Response caching to avoid reprocessing

- [ ] REST API for remote access

- [ ] Model comparison tools

- [ ] GUI interface for non-technical users

- [ ] Extended file format support (PDF, TXT, MD)

  

## 📝 License

  

Unlicensed

  

## 🤝 Contributing

  

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

  

## 📧 Contact

  

gm.carelli@unesp.br

  

---

  

**Note**: This project is under active development. Features and APIs may change.

  
  
**