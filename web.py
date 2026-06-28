from flask import Flask, render_template

from src.vcc.auditor.tinfoil_sync import TinfoilSync
from src.vcc.database import Database
from src.vcc.repository import Repository

app = Flask(__name__)


@app.route("/")
def index():

    database = Database("data/vcc.sqlite")
    repository = Repository(database)

    stats = repository.statistics()

    return render_template(
        "index.html",
        stats=stats,
    )


@app.route("/refresh-titledb", methods=["POST"])
def refresh_titledb():

    database = Database("data/vcc.sqlite")

    from src.vcc.services.sync_service import SyncService

    count = SyncService(database).run()

    return render_template(
        "refresh.html",
        count=count,
    )
    
if __name__ == "__main__":
    app.run(debug=True)