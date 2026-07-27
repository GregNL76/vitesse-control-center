from flask import Blueprint, g, jsonify

from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.game_service import GameService

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


def get_database():
    if "database" not in g:
        g.database = Database()
        g.database.initialize()
    return g.database


def get_repository():
    if "repository" not in g:
        g.repository = Repository(get_database())
    return g.repository


@api_bp.route("/games")
def games():

    return jsonify(
        GameService(get_repository()).games()
    )