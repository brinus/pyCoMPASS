Examples
========

This section lists runnable examples shipped in the repository.

Command-line examples
---------------------

Basic CLI example::

  $ python examples/basic_client.py

Simple example (auto-start local daemon)::

  $ python examples/simple_client.py
  FSM State: FSM state: Idle (terminal: no)
  Create Project Result: OK: Idle -> ProjectOpen | Project created successfully. Project is ready.

Notes
-----

- `--daemon-path` (or the hardcoded path in `simple_client.py`) must point to the executable file, not to a directory.
- Auto-start is only attempted for localhost connections.
