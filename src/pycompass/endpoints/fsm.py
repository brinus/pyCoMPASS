from __future__ import annotations

from pycompass.config import API_PREFIX
from pycompass.models.fsm_state import FsmState
from pycompass.transport.http import HttpTransport


def get_state(transport: HttpTransport) -> FsmState:
    data = transport.get_json(f"{API_PREFIX}/fsm/state")
    return FsmState.from_dict(data)
