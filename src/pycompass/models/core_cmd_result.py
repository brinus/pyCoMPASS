from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CoreCmdResult:
    success: bool
    old_state: str
    current_state: str
    message: str

    def __str__(self) -> str:
        status = "OK" if self.success else "FAILED"
        msg = self.message.strip() if self.message else ""
        if msg:
            return f"{status}: {self.old_state} -> {self.current_state} | {msg}"
        return f"{status}: {self.old_state} -> {self.current_state}"

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "CoreCmdResult":
        return CoreCmdResult(
            success=bool(data.get("success", False)),
            old_state=str(data.get("old_state", "")),
            current_state=str(data.get("current_state", "")),
            message=str(data.get("message", "")),
        )
