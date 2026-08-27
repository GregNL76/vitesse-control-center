"""
Vitesse Control Center

Main entry point.
"""

import subprocess
import sys

from src.vcc.config import PROJECT_ROOT
from src.vcc.logger import get_logger
from src.vcc.tasks import ApplicationTask


def restart_web_server(logger):
    web_script = PROJECT_ROOT / "web.py"
    try:
        result = subprocess.run(
            [sys.executable, str(web_script), "--background"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except OSError:
        logger.exception("Could not start the VCC web launcher.")
        return
    except subprocess.TimeoutExpired:
        logger.error("VCC web launcher did not finish within 15 seconds.")
        return

    if result.stdout.strip():
        logger.info("VCC web launcher output:\n%s", result.stdout.strip())
    if result.returncode != 0:
        logger.error(
            "VCC web launcher exited with status %s: %s",
            result.returncode,
            result.stderr.strip(),
        )


def main():

    logger = get_logger()

    logger.info("===================================")
    logger.info("Vitesse Control Center")
    logger.info("===================================")

    ApplicationTask().execute()
    restart_web_server(logger)

    logger.info("")
    logger.info("Done.")


if __name__ == "__main__":
    main()
