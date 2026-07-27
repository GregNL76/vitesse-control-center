from flask import Blueprint, g, render_template

from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.dashboard_service import DashboardService
from src.vcc.services.sync_service import SyncService

dashboard_bp = Blueprint("dashboard", __name__)


def get_database():
    if "database" not in g:
        g.database = Database()
        g.database.initialize()
    return g.database


def get_repository():
    if "repository" not in g:
        g.repository = Repository(get_database())
    return g.repository


def get_dashboard_service():
    if "dashboard_service" not in g:
        g.dashboard_service = DashboardService(get_repository())
    return g.dashboard_service


def get_sync_service():
    if "sync_service" not in g:
        g.sync_service = SyncService(get_database())
    return g.sync_service


def close_database(error=None):
    database = g.pop("database", None)
    if database is not None:
        database.close()


@dashboard_bp.route("/")
def index():

    dashboard_service = get_dashboard_service()

    return render_template(
        "dashboard.html",
        stats=dashboard_service.statistics(),
        health=dashboard_service.library_health(),
        activity=dashboard_service.recent_activity(),
    )


@dashboard_bp.route("/refresh-titledb", methods=["POST"])
def refresh_titledb():

    count = get_sync_service().run()

    return render_template(
        "refresh.html",
        count=count,
    )