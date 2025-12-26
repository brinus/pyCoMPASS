# Examples

Run examples from the repository root.

```bash
pip install -e .
python examples/basic_client.py --ip-address 127.0.0.1 --port 18080
python examples/basic_client.py --create-project /tmp/compass_project
python examples/basic_client.py --shutdown

# Auto-start local daemon (only when connecting to localhost)
python examples/basic_client.py --daemon-path ../CoMPASS-Core/install/bin/CoMPASS-Core

# Note: --daemon-path must point to the executable file (e.g. .../install/bin/CoMPASS-Core),
# not the install/bin directory.
```
