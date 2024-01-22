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

bp = Blueprint("io", __name__, url_prefix="/io")


def before_first_request():
    bp.db = current_app.extensions["db"]


@bp.route("/import/directory/<path>")
def import_from_directory(path: str):
    res = bp.db.import_from_directory(path)
    return res
