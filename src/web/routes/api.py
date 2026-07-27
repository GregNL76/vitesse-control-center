from flask import Blueprint, jsonify

from src.vcc.services.game_service import GameService

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api_bp.route("/games")
def games():

    return jsonify(
        GameService().games()
    )