from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from pycompass.exceptions import ApiError, TransportError


@dataclass
class HttpTransport:
    base_url: str
    timeout: float = 5.0

    def __post_init__(self) -> None:
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def close(self) -> None:
        self._client.close()

    def get_json(self, path: str) -> Dict[str, Any]:
        try:
            r = self._client.get(path)
        except httpx.ConnectError as e:
            raise TransportError("GET", self.base_url, "Connection refused") from e
        except httpx.TimeoutException as e:
            raise TransportError("GET", self.base_url, "Request timed out") from e
        except httpx.RequestError as e:
            raise TransportError("GET", self.base_url, f"Network error: {e}") from e

        if r.status_code >= 400:
            raise ApiError("GET", str(r.request.url), r.status_code, "Request failed", r.text)
        return r.json()

    def post_json(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> httpx.Response:
        try:
            r = self._client.post(path, json=json_body)
        except httpx.ConnectError as e:
            raise TransportError("POST", self.base_url, "Connection refused") from e
        except httpx.TimeoutException as e:
            raise TransportError("POST", self.base_url, "Request timed out") from e
        except httpx.RequestError as e:
            raise TransportError("POST", self.base_url, f"Network error: {e}") from e

        if r.status_code >= 400:
            raise ApiError("POST", str(r.request.url), r.status_code, "Request failed", r.text)
        return r
