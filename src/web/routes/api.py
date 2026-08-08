from flask import Blueprint, g, jsonify

from src.vcc.database import Database
from src.vcc.repository import Repository

from src.vcc.services.game_service import GameService
from src.vcc.services.update_service import UpdateService


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
        GameService(get_database()).games_api()
    )

@api_bp.route("/dlc")
def dlc():
    return jsonify(
        GameService(get_database()).dlcs()
    )
    
@api_bp.route("/missing-updates")
def missing_updates():
    return jsonify(
        UpdateService(get_repository()).missing_updates()
    )


@api_bp.route("/orphan-updates")
def orphan_updates():
    return jsonify(
        UpdateService(get_repository()).orphan_updates()
    )


@api_bp.route("/duplicate-updates")
def duplicate_updates():

    return jsonify(
        GameService(get_database()).duplicate_updates()
    )