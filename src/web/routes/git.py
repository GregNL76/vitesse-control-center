from flask import Blueprint, render_template, request

from src.vcc.services.git_service import GitService

git_bp = Blueprint("git", __name__)


@git_bp.route("/git", methods=["GET", "POST"])
def git():

    service = GitService()
    output = None

    if request.method == "POST":

        commit_message = request.form.get("commit_message", "")

        try:
            output = service.commit_and_push(commit_message)
        except RuntimeError as exc:
            output = str(exc)

    status = service.status()

    return render_template(
        "git.html",
        status=status,
        output=output,
    )
