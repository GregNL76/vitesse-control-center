"""
Full refresh task.
"""

import subprocess
import sys

from src.vcc.config import (
    VITESSESHOP_REFRESH_SCRIPT,
    VITESSESHOP_REFRESH_TIMEOUT_SECONDS,
)

from .base import BaseTask
from .run_audits import RunAuditsTask
from .scan_library import ScanLibraryTask
from .sync_titledb import SyncTitleDBTask


class FullRefreshTask(BaseTask):
    """
    Executes a complete VCC refresh.
    """

    @staticmethod
    def _summarize_output(stdout, stderr):

        output = "\n".join(
            part.strip() for part in [stdout, stderr] if part and str(part).strip()
        )

        if not output:
            return "No output captured."

        lines = [line.strip() for line in output.splitlines() if line.strip()]
        if not lines:
            return "No output captured."

        return lines[-5:]

    def _run_vitesseshop_refresh(self):

        if not VITESSESHOP_REFRESH_SCRIPT.exists():
            message = (
                f"VitesseShop refresh script not found at "
                f"{VITESSESHOP_REFRESH_SCRIPT}."
            )
            self.logger.error(message)
            return "failed", message

        try:
            result = subprocess.run(
                [sys.executable, str(VITESSESHOP_REFRESH_SCRIPT)],
                capture_output=True,
                text=True,
                timeout=VITESSESHOP_REFRESH_TIMEOUT_SECONDS,
                check=False,
            )

            if result.stdout:
                self.logger.info(
                    "VitesseShop refresh stdout:\n%s", result.stdout.strip()
                )
            if result.stderr:
                self.logger.warning(
                    "VitesseShop refresh stderr:\n%s", result.stderr.strip()
                )

            if result.returncode == 0:
                self.logger.info("VitesseShop refresh succeeded.")
                return "success", "VitesseShop refresh succeeded."

            message = (
                f"VitesseShop refresh failed with exit code " f"{result.returncode}."
            )
            self.logger.error(message)
            return "failed", message

        except subprocess.TimeoutExpired as exc:
            message = (
                f"VitesseShop refresh timed out after "
                f"{VITESSESHOP_REFRESH_TIMEOUT_SECONDS} seconds."
            )
            self.logger.error(message)
            if exc.stdout:
                self.logger.error(
                    "VitesseShop refresh timed out stdout:\n%s", exc.stdout.strip()
                )
            if exc.stderr:
                self.logger.error(
                    "VitesseShop refresh timed out stderr:\n%s", exc.stderr.strip()
                )
            return "timeout", message

        except Exception as exc:
            message = "VitesseShop refresh failed: " f"{type(exc).__name__}: {exc}"
            self.logger.exception(message)
            return "failed", message

    def run(self):

        try:
            ScanLibraryTask(
                self.database,
                self.repository,
            ).run()

            SyncTitleDBTask(
                self.database,
                self.repository,
            ).run()

            RunAuditsTask(
                self.database,
                self.repository,
            ).run()

            self.logger.info("VCC refresh succeeded.")
            vcc_status = "success"
            vcc_summary = "VCC refresh succeeded."

        except Exception:
            self.logger.exception("VCC refresh failed.")
            raise

        vitesseshop_status, vitesseshop_summary = self._run_vitesseshop_refresh()

        self.logger.info("VCC refresh status: %s", vcc_status)
        self.logger.info("VitesseShop refresh status: %s", vitesseshop_status)

        return {
            "vcc_refresh": vcc_status,
            "vitesseshop_refresh": vitesseshop_status,
            "summary": f"{vcc_summary} {vitesseshop_summary}",
        }
