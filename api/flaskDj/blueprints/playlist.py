import functools

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("playlist", __name__, url_prefix="/playlist")


def before_first_request():
    bp.db = DatabaseService(DatabaseService(current_app.config["DATABASE"]))


@bp.route("/add/<name>")
def add_playlist(name: str):
    return bp.db.add_playlist(name)


@bp.route("/delete/<name>")
def delete_playlist(name: str):
    return bp.db.delete_playlist(name)
