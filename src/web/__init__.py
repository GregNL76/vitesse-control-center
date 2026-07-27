from flask import Flask

from src.vcc.config import PROJECT_ROOT
from src.web.routes.dashboard import dashboard_bp
from src.web.routes.games import games_bp
from src.web.routes.api import api_bp
from src.web.routes.git import git_bp

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

    return app