from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class CoMPASSError(Exception):
    """Base error for pyCoMPASS."""


@dataclass
class DaemonStartError(CoMPASSError):
    daemon_path: str
    message: str

    def __str__(self) -> str:
        return f"{self.message} (daemon_path={self.daemon_path})"


@dataclass
class TransportError(CoMPASSError):
    method: str
    base_url: str
    message: str

    def __str__(self) -> str:
        return f"{self.message} (base_url={self.base_url}, method={self.method})"


@dataclass
class ApiError(CoMPASSError):
    method: str
    url: str
    status_code: int
    message: str
    response_text: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.method} {self.url} -> {self.status_code}: {self.message}"
        if self.response_text:
            return f"{base}\n{self.response_text}"
        return base
