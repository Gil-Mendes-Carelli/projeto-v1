from typing import Protocol


class HostClient(Protocol):
    def connect_to_host(self, host_url: str) -> "HostClient": ...
