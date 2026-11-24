"""Platform-specific process management used by SDR source workers."""

import os
import signal
import subprocess


def get_process_start_options(is_windows=None):
    """Return Popen options that isolate an SDR process group on the host OS."""
    if is_windows is None:
        is_windows = os.name == "nt"

    if is_windows:
        # CTRL_BREAK_EVENT can be sent to processes started in this group.
        creation_flag = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
        return {"creationflags": creation_flag}

    return {"start_new_session": True}


def stop_process(process, monitor=None, timeout=10, is_windows=None):
    """Stop an SDR process group, force-terminating it if it ignores shutdown.

    Returns True when the process had to be force-terminated.
    """
    if process is None:
        return False

    if is_windows is None:
        is_windows = os.name == "nt"

    if is_windows:
        break_event = getattr(signal, "CTRL_BREAK_EVENT", None)
        try:
            if break_event is None:
                process.terminate()
            else:
                process.send_signal(break_event)
        except (OSError, ProcessLookupError, ValueError):
            try:
                process.terminate()
            except (OSError, ProcessLookupError):
                pass
    else:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass

    if monitor is None:
        return False

    monitor.join(timeout)
    if not monitor.is_alive():
        return False

    if is_windows:
        try:
            process.kill()
        except (OSError, ProcessLookupError):
            pass
    else:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass

    return True
