import calendar
from datetime import datetime, timedelta, timezone

from flask import Blueprint, g, redirect, render_template, url_for

from src.vcc.database import Database
from src.vcc.services.report_service import ReportService

placeholders_bp = Blueprint("placeholders", __name__)

WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def format_request_timestamp(value):
    if not value:
        return "-"

    try:
        timestamp = datetime.fromisoformat(str(value))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        year = timestamp.year
        march_last_day = calendar.monthrange(year, 3)[1]
        october_last_day = calendar.monthrange(year, 10)[1]
        dst_start_day = march_last_day - (
            (datetime(year, 3, march_last_day).weekday() + 1) % 7
        )
        dst_end_day = october_last_day - (
            (datetime(year, 10, october_last_day).weekday() + 1) % 7
        )
        dst_start = datetime(year, 3, dst_start_day, 1, tzinfo=timezone.utc)
        dst_end = datetime(year, 10, dst_end_day, 1, tzinfo=timezone.utc)
        local_timezone = (
            timezone(timedelta(hours=2), "CEST")
            if dst_start <= timestamp.astimezone(timezone.utc) < dst_end
            else timezone(timedelta(hours=1), "CET")
        )
        timestamp = timestamp.astimezone(local_timezone)
        return (
            f"{WEEKDAYS[timestamp.weekday()]} {MONTHS[timestamp.month - 1]} "
            f"{timestamp.day}, {timestamp.year} - {timestamp:%H:%M}u. {timestamp:%Z}"
        )
    except ValueError:
        return str(value)


def get_database():
    if "database" not in g:
        g.database = Database()
        g.database.initialize()
    return g.database


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
    database = get_database()
    requested_titles = database.connection.execute("""
        SELECT id, requester_name, title, request_type, created_at
        FROM game_requests
        WHERE status = 'PENDING'
        ORDER BY created_at DESC
        """).fetchall()
    completed_requests = database.connection.execute("""
        SELECT requester_name, title, request_type, created_at, completed_at
        FROM game_requests
        WHERE status = 'COMPLETED'
        ORDER BY completed_at DESC
        """).fetchall()

    requested_titles = [dict(item) for item in requested_titles]
    completed_requests = [dict(item) for item in completed_requests]
    for item in requested_titles + completed_requests:
        item["created_at_display"] = format_request_timestamp(item["created_at"])
        item["completed_at_display"] = format_request_timestamp(
            item.get("completed_at")
        )

    invalid_updates = service.invalid_update_title_ids()

    versions_without_v = service.update_versions_without_v()

    invalid_version_blocks = service.invalid_update_version_blocks()

    invalid_base_versions = service.invalid_base_version_blocks()

    return render_template(
        "reports.html",
        invalid_updates=invalid_updates,
        versions_without_v=versions_without_v,
        invalid_version_blocks=invalid_version_blocks,
        invalid_base_versions=invalid_base_versions,
        requested_titles=requested_titles,
        completed_requests=completed_requests,
    )


@placeholders_bp.route("/reports/requests/<int:request_id>/complete", methods=["POST"])
def complete_request(request_id):
    database = get_database()
    database.connection.execute(
        """
        UPDATE game_requests
        SET status = 'COMPLETED', completed_at = ?
        WHERE id = ? AND status = 'PENDING'
        """,
        (datetime.now(timezone.utc).isoformat(), request_id),
    )
    database.connection.commit()
    return redirect(url_for("placeholders.reports"))


@placeholders_bp.route("/reports/requests/completed/flush", methods=["POST"])
def flush_completed_requests():
    database = get_database()
    database.connection.execute("DELETE FROM game_requests WHERE status = 'COMPLETED'")
    database.connection.commit()
    return redirect(url_for("placeholders.reports"))


@placeholders_bp.route("/settings")
def settings():
    return render_template("settings.html")
