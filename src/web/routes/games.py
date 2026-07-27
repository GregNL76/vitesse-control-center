from flask import Blueprint, render_template

games_bp = Blueprint("games", __name__)


@games_bp.route("/games")
def games():
    return render_template("games.html")