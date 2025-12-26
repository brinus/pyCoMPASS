Usage
=====

Install (editable) from the repo root::

  pip install -e .

Basic example::

  python examples/basic_client.py

Simple example (auto-start local daemon)::

  python examples/simple_client.py

Programmatic usage::

  from pycompass import CoMPASSClient

  with CoMPASSClient(ip_address="127.0.0.1", port=18080) as c:
      print(c.fsm_state())
      print(c.create_project("/tmp/compass_project"))

Auto-start local daemon (optional)
--------------------------------

If you are connecting to localhost and you want Python to start/stop the daemon automatically, pass a path to the `CoMPASS-Core` binary::

  from pycompass import CoMPASSClient

  with CoMPASSClient(
      ip_address="127.0.0.1",
      port=18080,
      auto_start_local_daemon=True,
      daemon_path="/path/to/CoMPASS-Core",
  ) as c:
      print(c.fsm_state())

If the daemon is already running, it will NOT be stopped when the client closes.

Full script example
-------------------

The `examples/simple_client.py` script demonstrates how to:

- auto-start the daemon locally (only when connecting to localhost)
- query the FSM state
- create a project

Example code::

  from pycompass import CoMPASSClient
  from pycompass.exceptions import DaemonStartError, TransportError

  try:
    with CoMPASSClient(
      ip_address="127.0.0.1",
      port=18080,
      auto_start_local_daemon=True,
      daemon_path="../CoMPASS-Core/install/bin/CoMPASS-Core",
    ) as client:
      print(client.fsm_state())
      print(client.create_project("/tmp/compass_project_example"))
  except (TransportError, DaemonStartError) as e:
    print(f"Error: {e}")
