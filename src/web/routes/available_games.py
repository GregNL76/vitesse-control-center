from __future__ import annotations

import math

from flask import Blueprint, render_template, request

from src.vcc.services.available_games_service import AvailableGamesService


available_games_bp = Blueprint("available_games", __name__)


@available_games_bp.route("/available-games")
def available_games():
    search = " ".join(request.args.get("q", "").split())
    page = max(1, request.args.get("page", 1, type=int))
    page_size = 100
    error = None

    try:
        catalog = AvailableGamesService().get()
    except Exception:
        catalog = {"games": [], "fetched_at": None, "stale": False}
        error = "The NSWGF game list is temporarily unavailable."

    games = catalog["games"]
    if search:
        search_key = search.casefold()
        games = [game for game in games if search_key in game["title"].casefold()]

    total = len(games)
    total_pages = max(1, math.ceil(total / page_size))
    page = min(page, total_pages)
    start = (page - 1) * page_size

    return render_template(
        "available_games.html",
        games=games[start:start + page_size],
        total=total,
        search=search,
        page=page,
        total_pages=total_pages,
        fetched_at=catalog.get("fetched_at"),
        stale=catalog.get("stale", False),
        error=error,
    )
