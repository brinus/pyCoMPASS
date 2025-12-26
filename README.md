# pyCoMPASS

Python client/bindings for the CoMPASS-Core REST API.

The goal of this repository is to provide client-side APIs that talk to the CoMPASS-Core daemon (HTTP), so user applications do not need to manually craft requests.

## Package layout

This repository uses the `src/` layout. The PyPI distribution name is configured in `pyproject.toml`, while the import name is the `pycompass` package.

Recommended structure (minimal but scalable):

```text
pyCoMPASS/
  pyproject.toml
  src/
    pycompass/
      __init__.py        # public exports
      client.py          # CoMPASSClient (high-level API)
      config.py          # base URL + API prefix constants
      exceptions.py      # typed errors
      transport/
        http.py          # httpx wrapper
      endpoints/
        fsm.py           # /fsm/state
        project.py       # /project/create
        system.py        # /shutdown
      models/
        fsm_state.py
        core_cmd_result.py
```

## Minimal usage

```python
from pycompass import CoMPASSClient

with CoMPASSClient(ip_address="127.0.0.1", port=18080) as c:
    print(c.fsm_state())
    print(c.create_project("/tmp/compass_project"))
```

## Documentation (Sphinx / Read the Docs)

Build docs locally:

```bash
pip install -e ".[docs]"
make -C docs html
open docs/_build/html/index.html
```

Read the Docs is configured via `readthedocs.yaml`.
