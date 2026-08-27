from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, request

from src.vcc.database import Database
from src.vcc.repository import Repository

from src.vcc.services.game_service import GameService
from src.vcc.services.update_service import UpdateService

api_bp = Blueprint("api", __name__, url_prefix="/api")


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
    return jsonify(GameService(get_database()).games_api())


@api_bp.route("/regions")
def regions():
    return jsonify(get_database().regions.as_map())


@api_bp.route("/dlc")
def dlc():
    return jsonify(GameService(get_database()).dlcs())


@api_bp.route("/missing-updates")
def missing_updates():
    return jsonify(UpdateService(get_repository()).missing_updates())


@api_bp.route("/orphan-updates")
def orphan_updates():
    return jsonify(UpdateService(get_repository()).orphan_updates())


@api_bp.route("/duplicate-updates")
def duplicate_updates():

    return jsonify(GameService(get_database()).duplicate_updates())


@api_bp.route("/requests", methods=["POST"])
def create_request():
    payload = request.get_json(silent=True) or request.form
    requester_name = " ".join(str(payload.get("name", "")).split())
    title = " ".join(str(payload.get("title", "")).split())
    request_type = str(payload.get("type", "")).upper()

    if not 2 <= len(requester_name) <= 60 or not 2 <= len(title) <= 160:
        return (
            jsonify({"error": "Name and title must be between 2 and 160 characters."}),
            400,
        )
    if request_type not in {"GAME", "UPDATE", "DLC"}:
        return jsonify({"error": "Invalid request type."}), 400

    database = get_database()
    database.connection.execute(
        """
        INSERT INTO game_requests (requester_name, title, request_type, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (requester_name, title, request_type, datetime.now(timezone.utc).isoformat()),
    )
    database.connection.commit()

    return jsonify({"status": "created"}), 201
