from flask import Blueprint, render_template

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
    return render_template("reports.html")


@placeholders_bp.route("/settings")
def settings():
    return render_template("settings.html")
