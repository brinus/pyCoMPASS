from __future__ import annotations

from pycompass.config import API_PREFIX
from pycompass.models.core_cmd_result import CoreCmdResult
from pycompass.transport.http import HttpTransport


def create_project(transport: HttpTransport, project_path: str) -> CoreCmdResult:
    r = transport.post_json(f"{API_PREFIX}/project/create", {"project_path": project_path})
    return CoreCmdResult.from_dict(r.json())
