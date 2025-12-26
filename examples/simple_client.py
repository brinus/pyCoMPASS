from pycompass import CoMPASSClient
from pycompass.exceptions import CoMPASSError, ApiError, DaemonStartError, TransportError

def main() -> int:
    try:
        with CoMPASSClient(
            ip_address="127.0.0.1",
            port=18080,
            auto_start_local_daemon=True,
            daemon_path=".path/to/compass_core_executable",
        ) as client:
            state = client.fsm_state()
            print("FSM State:", state)

            res = client.create_project("/tmp/compass_project_example")
            print("Create Project Result:", res)
    except TransportError as e:
        print(f"Transport Error: {e}")
        return 1
    except DaemonStartError as e:
        print(f"Daemon Start Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())