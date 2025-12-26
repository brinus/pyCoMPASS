from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Optional

from pycompass.exceptions import DaemonStartError


def _is_local_address(ip_address: str) -> bool:
    ip = (ip_address or "").strip().lower()
    return ip in {"127.0.0.1", "localhost", "::1"}


@dataclass
class DaemonHandle:
    """Represents a daemon process started by Python."""

    process: subprocess.Popen
    ip_address: str
    port: int

    def terminate(self, timeout: float = 2.0) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=timeout)


def maybe_start_local_daemon(
    *,
    ip_address: str,
    port: int,
    daemon_path: str | None,
    startup_timeout: float,
    is_ready: Callable[[], bool],
) -> Optional[DaemonHandle]:
    """Start CoMPASS-Core if (1) ip is local, (2) daemon_path is provided, (3) server is not ready.

    Returns a DaemonHandle only if Python started the daemon.
    """

    if not _is_local_address(ip_address):
        return None

    if not daemon_path:
        return None

    if os.path.isdir(daemon_path):
        raise DaemonStartError(
            daemon_path,
            "daemon_path points to a directory; expected the CoMPASS-Core executable",
        )
    if not os.path.isfile(daemon_path):
        raise DaemonStartError(
            daemon_path,
            "daemon_path does not exist or is not a file",
        )
    if not os.access(daemon_path, os.X_OK):
        raise DaemonStartError(
            daemon_path,
            "daemon_path is not executable (check permissions or rebuild/install)",
        )

    # If already running, do nothing.
    if is_ready():
        return None

    # Start daemon.
    try:
        proc = subprocess.Popen(
            [
                daemon_path,
                "-A",
                ip_address,
                "-P",
                str(port),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except PermissionError as e:
        raise DaemonStartError(daemon_path, "Permission denied while starting daemon") from e

    deadline = time.monotonic() + max(0.1, startup_timeout)
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise DaemonStartError(
                daemon_path,
                f"Daemon exited early with code {proc.returncode}",
            )
        if is_ready():
            return DaemonHandle(proc, ip_address, port)
        time.sleep(0.1)

    raise DaemonStartError(
        daemon_path,
        f"Timed out waiting for daemon to become ready (timeout={startup_timeout}s)",
    )
