from flask import Blueprint, render_template

from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.dashboard_service import DashboardService
from src.vcc.services.sync_service import SyncService

dashboard_bp = Blueprint("dashboard", __name__)


database = Database()
repository = Repository(database)

dashboard_service = DashboardService(repository)
sync_service = SyncService(database)


@dashboard_bp.route("/")
def index():

    stats = dashboard_service.statistics()

    return render_template(
        "dashboard.html",
        stats=stats,
    )


@dashboard_bp.route("/refresh-titledb", methods=["POST"])
def refresh_titledb():

    count = sync_service.run()

    return render_template(
        "refresh.html",
        count=count,
    )