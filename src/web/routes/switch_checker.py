from flask import Blueprint, render_template, request

from src.vcc.switch_serial import check_serial


switch_checker_bp = Blueprint("switch_checker", __name__)


@switch_checker_bp.route("/switch-checker", methods=["GET", "POST"])
def switch_checker():
    result = None
    serial = ""

    if request.method == "POST":
        serial = request.form.get("serial", "")
        result = check_serial(serial)

    return render_template(
        "switch_checker.html",
        result=result,
        serial=serial,
    )