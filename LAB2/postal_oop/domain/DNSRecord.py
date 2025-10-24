from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DNSRecord:
    """Условная конфигурационная запись (ключ=значение) для почтовой сети.
    Используем как простой KV-конфиг, не интернет-DNS.
    """
    key: str
    value: str

    def as_tuple(self) -> tuple[str, str]:
        return (self.key, self.value)

    def matches(self, prefix: str) -> bool:
        return self.key.startswith(prefix)
