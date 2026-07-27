from flask import Blueprint, render_template

from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.sync_service import SyncService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():

    database = Database("data/vcc.sqlite")
    repository = Repository(database)

    stats = repository.statistics()

    return render_template(
        "dashboard.html",
        stats=stats,
    )


@dashboard_bp.route("/refresh-titledb", methods=["POST"])
def refresh_titledb():

    database = Database("data/vcc.sqlite")

    count = SyncService(database).run()

    return render_template(
        "refresh.html",
        count=count,
    )