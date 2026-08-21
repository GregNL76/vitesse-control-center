from flask import Blueprint, render_template

from src.vcc.services.report_service import ReportService


placeholders_bp = Blueprint("placeholders", __name__)

@placeholders_bp.route("/missing-updates")
def missing_updates():
    return render_template("missing_updates.html")


@placeholders_bp.route("/orphans")
def orphans():
    return render_template("orphans.html")


@placeholders_bp.route("/duplicates")
def duplicates():
    return render_template("duplicates.html")


@placeholders_bp.route("/reports")
def reports():

    service = ReportService()

    invalid_updates = (
        service.invalid_update_title_ids()
    )

    versions_without_v = (
        service.update_versions_without_v()
    )

    invalid_version_blocks = (
        service.invalid_update_version_blocks()
    )

    return render_template(
        "reports.html",
        invalid_updates=invalid_updates,
        versions_without_v=versions_without_v,
        invalid_version_blocks=invalid_version_blocks,
    )


@placeholders_bp.route("/settings")
def settings():
    return render_template("settings.html")
