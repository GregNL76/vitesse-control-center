from flask import Blueprint, jsonify

from src.vcc.tasks import (
    FullRefreshTask,
    RunAuditsTask,
    ScanLibraryTask,
    SyncTitleDBTask,
)

tasks_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/api/tasks",
)


@tasks_bp.post("/scan-library")
def scan_library():

    ScanLibraryTask().execute()

    return jsonify(
        {
            "success": True,
            "message": "Library scan completed.",
        }
    )


@tasks_bp.post("/refresh-titledb")
def refresh_titledb():

    SyncTitleDBTask().execute()

    return jsonify(
        {
            "success": True,
            "message": "TitleDB synchronized.",
        }
    )


@tasks_bp.post("/run-audits")
def run_audits():

    RunAuditsTask().execute()

    return jsonify(
        {
            "success": True,
            "message": "Audits completed.",
        }
    )


@tasks_bp.post("/full-refresh")
def full_refresh():

    FullRefreshTask().execute()

    return jsonify(
        {
            "success": True,
            "message": "Full refresh completed.",
        }
    )