import argparse
import os
import signal
import subprocess
import sys
import time

from src.vcc.logger import LOG_FILE, get_logger
from src.web import create_app

app = create_app()
logger = get_logger("VCC Web")

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)
app.logger.propagate = False


def recent_log_lines(limit=8):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as log_file:
            return log_file.readlines()[-limit:]
    except OSError:
        return []


def launch_background_server():
    console_log = LOG_FILE.with_name("vcc-web-console.log")
    stop_existing_server()
    logger.info("Launching background VCC web server; console log: %s", console_log)
    try:
        with open(console_log, "a", encoding="utf-8") as output:
            process = subprocess.Popen(
                [sys.executable, __file__, "--serve"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=output,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
    except OSError:
        logger.exception("Could not launch the background VCC web server.")
        print("VCC web process could not be started. Check vcc.log.")
        return

    time.sleep(1)
    if process.poll() is None:
        logger.info("Started background VCC web process %s.", process.pid)
        print(f"VCC web process started (PID {process.pid}).")
    else:
        print(
            f"VCC web process stopped during startup (exit code {process.returncode})."
        )

    print("Recent VCC log:")
    print("".join(recent_log_lines()).rstrip())


def stop_existing_server():
    """Stop a previous VCC web process before binding the dashboard port."""
    if os.name != "posix" or not os.path.isdir("/proc"):
        logger.warning("Port cleanup skipped: /proc is not available.")
        return

    script_path = os.path.realpath(__file__)
    stopped_processes = []
    for entry in os.scandir("/proc"):
        if not entry.name.isdigit() or int(entry.name) == os.getpid():
            continue

        try:
            with open(os.path.join(entry.path, "cmdline"), "rb") as command_file:
                command = (
                    command_file.read().decode("utf-8", "replace").replace("\0", " ")
                )
            if script_path not in command:
                continue
            os.kill(int(entry.name), signal.SIGTERM)
            stopped_processes.append(entry.name)
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        except OSError as error:
            logger.warning("Could not stop VCC web process %s: %s", entry.name, error)

    if stopped_processes:
        logger.info(
            "Stopped previous VCC web process(es): %s", ", ".join(stopped_processes)
        )
        time.sleep(0.5)


def serve():
    logger.info("Starting VCC web server on port 5050.")
    try:
        app.run(
            host="0.0.0.0",
            port=5050,
            debug=False,
            use_reloader=False,
        )
    except OSError:
        logger.exception("VCC web server stopped unexpectedly.")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--background", action="store_true")
    parser.add_argument("--serve", action="store_true")
    arguments = parser.parse_args()
    logger.info(
        "VCC web launcher invoked (background=%s, serve=%s).",
        arguments.background,
        arguments.serve,
    )

    if arguments.background:
        launch_background_server()
    elif arguments.serve:
        serve()
    else:
        stop_existing_server()
        serve()
