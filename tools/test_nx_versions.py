"""Regression checks for the nx-versions cache and auditor integration."""

import sys
import tempfile
import types
from pathlib import Path

if "requests" not in sys.modules:
    requests = types.ModuleType("requests")
    requests.RequestException = Exception
    sys.modules["requests"] = requests

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.sources.nx_versions import NxVersionsSource


class Response:
    status_code = 200
    text = "id|version\n0100ABCDE1234800|131072\ninvalid|999\n"
    headers = {"ETag": "test-etag", "Last-Modified": "test-date"}

    def raise_for_status(self):
        return None


class Session:
    def get(self, url, headers, timeout):
        assert "nx-versions" in url
        assert timeout == 30
        return Response()


class Source:
    def latest_version(self, title_id):
        assert title_id == "0100ABCDE1234800"
        return 131072


class Repository:
    def games_with_latest_versions(self):
        return [{
            "title_id": "0100ABCDE1234000",
            "name": "Example Game",
            "installed_version": 65536,
            "latest_version": 65536,
        }]


with tempfile.TemporaryDirectory() as temporary_directory:
    cache = Path(temporary_directory) / "nx_versions.json"
    source = NxVersionsSource(cache_file=cache, session=Session())
    result = source.sync()
    assert result["titles"] == 1
    assert result["cached"] is False
    assert source.latest_version("0100abcde1234800") == 131072

report = UpdateAuditor(Repository(), nx_versions=Source()).audit()
assert len(report) == 1
assert report[0]["latest"] == 131072
assert report[0]["tinfoil_latest"] == 65536
assert report[0]["nx_versions_latest"] == 131072
assert report[0]["sources_disagree"] is True

print("nx-versions cache and update-auditor integration: OK")
