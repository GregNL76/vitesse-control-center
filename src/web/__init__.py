from flask import Flask, g

from src.vcc.config import PROJECT_ROOT
from src.vcc.database import Database
from src.vcc.repository import Repository
from src.vcc.services.dashboard_service import DashboardService
from src.web.routes.dashboard import dashboard_bp
from src.web.routes.games import games_bp
from src.web.routes.api import api_bp
from src.web.routes.git import git_bp
from src.web.routes.placeholders import placeholders_bp

BASE_DIR = PROJECT_ROOT


def create_app():

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(git_bp)
    app.register_blueprint(placeholders_bp)

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

    @app.context_processor
    def inject_activity_events():
        return {
            "activity_events": get_dashboard_service().recent_activity(),
        }

    @app.teardown_appcontext
    def close_database(exception=None):
        from src.web.routes.dashboard import close_database as dashboard_close_database

        dashboard_close_database(exception)

    return app