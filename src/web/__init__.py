from flask import Flask, g

from src.web.routes.dashboard import dashboard_bp
from src.vcc.config import PROJECT_ROOT
from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.dashboard_service import DashboardService
from src.web.routes.games import games_bp
from src.web.routes.api import api_bp
from src.web.routes.git import git_bp
from src.web.routes.placeholders import placeholders_bp
from src.web.routes.tasks import tasks_bp
from src.web.routes.available_games import available_games_bp

from pathlib import Path

WEB_ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------

def create_app():

    app = Flask(

        __name__,

        template_folder=str(WEB_ROOT / "templates"),

        static_folder=str(WEB_ROOT / "static"),

    )

    # -------------------------------------------------------------

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(api_bp)

    app.register_blueprint(games_bp)

    app.register_blueprint(git_bp)

    app.register_blueprint(placeholders_bp)
    
    app.register_blueprint(tasks_bp)

    app.register_blueprint(available_games_bp)

    # -------------------------------------------------------------
    # Shared services
    # -------------------------------------------------------------

    def get_database():

        if "database" not in g:

            database = Database()

            database.initialize()

            g.database = database

        return g.database


    def get_dashboard_service():

        if "dashboard_service" not in g:

            g.dashboard_service = DashboardService(

                get_database()

            )

        return g.dashboard_service

    # -------------------------------------------------------------
    # Global template variables
    # -------------------------------------------------------------

    @app.context_processor
    def inject_globals():

        dashboard = get_dashboard_service().overview()

        return {

            "statistics": dashboard["statistics"],

        }

    # -------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------

    @app.teardown_appcontext
    def close_database(exception=None):

        database = g.pop("database", None)

        if database is not None:

            database.close()

    return app
