from __future__ import annotations

from typing import Optional

from pycompass.config import IP_ADDRESS, PORT
from pycompass.daemon import DaemonHandle, maybe_start_local_daemon
from pycompass.endpoints import fsm as fsm_endpoints
from pycompass.endpoints import project as project_endpoints
from pycompass.endpoints import system as system_endpoints
from pycompass.exceptions import TransportError
from pycompass.models.core_cmd_result import CoreCmdResult
from pycompass.models.fsm_state import FsmState
from pycompass.transport.http import HttpTransport


class CoMPASSClient:
    """High-level client for the CoMPASS-Core REST API."""

    def __init__(
        self,
        ip_address: str = IP_ADDRESS,
        port: int = PORT,
        timeout: float = 5.0,
        *,
        auto_start_local_daemon: bool = False,
        daemon_path: str | None = None,
        startup_timeout: float = 5.0,
    ):
        base_url = f"http://{ip_address}:{port}"
        self._transport = HttpTransport(base_url=base_url, timeout=timeout)

        self._owned_daemon: Optional[DaemonHandle] = None

        if auto_start_local_daemon:
            def _ready() -> bool:
                try:
                    self._transport.get_json("/compass/api/v1/fsm/state")
                    return True
                except TransportError:
                    return False

            self._owned_daemon = maybe_start_local_daemon(
                ip_address=ip_address,
                port=port,
                daemon_path=daemon_path,
                startup_timeout=startup_timeout,
                is_ready=_ready,
            )

    def close(self) -> None:
        # If Python started the daemon, Python should stop it.
        if self._owned_daemon is not None:
            try:
                # Prefer a graceful shutdown via API.
                self.shutdown()
            except Exception:
                # Best effort: fall back to terminating the process.
                self._owned_daemon.terminate()
            finally:
                self._owned_daemon = None

        self._transport.close()

    def fsm_state(self) -> FsmState:
        return fsm_endpoints.get_state(self._transport)

    def create_project(self, project_path: str) -> CoreCmdResult:
        return project_endpoints.create_project(self._transport, project_path)

    def shutdown(self) -> str:
        return system_endpoints.shutdown(self._transport)

    def __enter__(self) -> "CoMPASSClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
