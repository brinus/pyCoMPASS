from __future__ import annotations

from pycompass.config import API_PREFIX
from pycompass.transport.http import HttpTransport


def shutdown(transport: HttpTransport) -> str:
    r = transport.post_json(f"{API_PREFIX}/shutdown")
    return r.text
