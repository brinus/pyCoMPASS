from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class FsmState:
    state: str
    is_terminal: bool

    def __str__(self) -> str:
        term = "yes" if self.is_terminal else "no"
        return f"FSM state: {self.state} (terminal: {term})"

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "FsmState":
        return FsmState(
            state=str(data.get("state", "")),
            is_terminal=bool(data.get("is_terminal", False)),
        )
