from typing import Protocol, TypeVar, Generic, List, Dict, Any

TClient = TypeVar("TClient")

class HostConnector(Protocol, Generic[TClient]):
    def connect_to_host(self, host_url:str) -> TClient | None: ...
    

class LLMTools(Protocol): 
    def list_models(self) -> str: ...
    
    def create_model(self, base_model: str, model_name: str, system_role:str) -> None: ...
    
    def chat_with_model(self, model_name: str, messages: List[Dict[str, Any]]) -> str: ...