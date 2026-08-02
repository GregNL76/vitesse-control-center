from flask import Blueprint, g, render_template

from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.dashboard_service import DashboardService
from src.vcc.services.sync_service import SyncService

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------

def get_database():

    if "database" not in g:

        g.database = Database()
        g.database.initialize()

    return g.database


# ---------------------------------------------------------------------
# Repository
# ---------------------------------------------------------------------

def get_repository():

    if "repository" not in g:

        g.repository = Repository(
            get_database()
        )

    return g.repository


# ---------------------------------------------------------------------
# Dashboard service
# ---------------------------------------------------------------------

def get_dashboard_service():

    if "dashboard_service" not in g:

        #
        # DashboardService gebruikt momenteel rechtstreeks
        # de Database.
        #
        # Mocht DashboardService later Repository gebruiken,
        # dan hoeft alleen deze functie aangepast te worden.
        #

        g.dashboard_service = DashboardService(
            get_database()
        )

    return g.dashboard_service


# ---------------------------------------------------------------------
# Sync service
# ---------------------------------------------------------------------

def get_sync_service():

    if "sync_service" not in g:

        g.sync_service = SyncService(
            get_database()
        )

    return g.sync_service


# ---------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------

@dashboard_bp.teardown_app_request
def close_database(error=None):

    database = g.pop("database", None)

    if database is not None:

        database.close()


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------

@dashboard_bp.route("/")
def index():

    dashboard = get_dashboard_service()

    data = dashboard.overview()

    return render_template(

        "dashboard.html",

        stats=data["statistics"],

        largest_games=data["largest_games"],

        missing_updates=data["missing_updates"],

    )


# ---------------------------------------------------------------------
# Refresh TitleDB
# ---------------------------------------------------------------------

@dashboard_bp.route(
    "/refresh-titledb",
    methods=["POST"],
)
def refresh_titledb():

    result = get_sync_service().run()

    return render_template(

        "refresh.html",

        result=result,

    )