from __future__ import annotations

import argparse

from pycompass import CoMPASSClient
from pycompass.exceptions import ApiError, DaemonStartError, TransportError


def main() -> int:
    parser = argparse.ArgumentParser(description="pyCoMPASS basic client example")
    parser.add_argument(
        "--ip-address",
        default="127.0.0.1",
        help="CoMPASS-Core IP address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=18080,
        help="CoMPASS-Core port (default: 18080)",
    )
    parser.add_argument(
        "--create-project",
        default=None,
        help="If provided, calls /project/create with this path",
    )
    parser.add_argument(
        "--shutdown",
        action="store_true",
        help="If set, calls /shutdown (stops the CoMPASS-Core daemon)",
    )
    parser.add_argument(
        "--daemon-path",
        default=None,
        help="If set, auto-starts CoMPASS-Core locally when not running (path to CoMPASS-Core binary)",
    )
    args = parser.parse_args()

    try:
        with CoMPASSClient(
            ip_address=args.ip_address,
            port=args.port,
            auto_start_local_daemon=bool(args.daemon_path),
            daemon_path=args.daemon_path,
        ) as client:
            state = client.fsm_state()
            print(state)

            if args.create_project:
                res = client.create_project(args.create_project)
                print(res)

            if args.shutdown:
                msg = client.shutdown()
                print("Shutdown:", msg)
    except TransportError as e:
        print(f"Error: {e}")
        print("Hint: is CoMPASS-Core running and reachable?")
        return 1
    except DaemonStartError as e:
        print(f"Error: {e}")
        print("Hint: pass the full path to the CoMPASS-Core executable (not the install/bin directory).")
        return 4
    except ApiError as e:
        print(f"Error: {e}")
        if e.status_code == 409:
            print("Hint: project already exists?")
            return 3
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
