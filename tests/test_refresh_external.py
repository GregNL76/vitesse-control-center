import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from src.vcc.tasks.full_refresh import FullRefreshTask


class FullRefreshTaskExternalScriptTests(unittest.TestCase):
    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.vcc.tasks.full_refresh.subprocess.run")
    @patch("src.vcc.tasks.full_refresh.RunAuditsTask.run")
    @patch("src.vcc.tasks.full_refresh.SyncTitleDBTask.run")
    @patch("src.vcc.tasks.full_refresh.ScanLibraryTask.run")
    def test_runs_external_script_after_successful_vcc_refresh(
        self,
        mock_scan_run,
        mock_sync_run,
        mock_audits_run,
        mock_subprocess_run,
        mock_exists,
    ):
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", "/tmp/script.py"],
            returncode=0,
            stdout="all good\n",
            stderr="",
        )

        result = FullRefreshTask().run()

        self.assertEqual(result["vcc_refresh"], "success")
        self.assertEqual(result["vitesseshop_refresh"], "success")
        mock_subprocess_run.assert_called_once()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.vcc.tasks.full_refresh.subprocess.run")
    @patch("src.vcc.tasks.full_refresh.RunAuditsTask.run")
    @patch("src.vcc.tasks.full_refresh.SyncTitleDBTask.run")
    @patch("src.vcc.tasks.full_refresh.ScanLibraryTask.run")
    def test_reports_external_script_failure_without_failing_vcc_refresh(
        self,
        mock_scan_run,
        mock_sync_run,
        mock_audits_run,
        mock_subprocess_run,
        mock_exists,
    ):
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", "/tmp/script.py"],
            returncode=7,
            stdout="partial\n",
            stderr="script exploded\n",
        )

        result = FullRefreshTask().run()

        self.assertEqual(result["vcc_refresh"], "success")
        self.assertEqual(result["vitesseshop_refresh"], "failed")
        self.assertIn("failed with exit code 7", result["summary"].lower())

    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.vcc.tasks.full_refresh.subprocess.run")
    @patch("src.vcc.tasks.full_refresh.RunAuditsTask.run")
    @patch("src.vcc.tasks.full_refresh.SyncTitleDBTask.run")
    @patch("src.vcc.tasks.full_refresh.ScanLibraryTask.run")
    def test_reports_external_script_timeout_separately(
        self,
        mock_scan_run,
        mock_sync_run,
        mock_audits_run,
        mock_subprocess_run,
        mock_exists,
    ):
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd=["python", "/tmp/script.py"],
            timeout=600,
            output="still running",
        )

        result = FullRefreshTask().run()

        self.assertEqual(result["vcc_refresh"], "success")
        self.assertEqual(result["vitesseshop_refresh"], "timeout")
        self.assertIn("timed out after 600 seconds", result["summary"].lower())


if __name__ == "__main__":
    unittest.main()
