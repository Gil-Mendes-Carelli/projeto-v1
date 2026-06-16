from typing import Protocol


class HostClient(Protocol):
    def connect_to_host(self, host_url: str) -> "HostClient": ...
    
    def chat(
        self,
        model_name: str,
        messages: list[dict[str, str]],
        options: dict[str, float] | None = None,
    ) -> str: ...
