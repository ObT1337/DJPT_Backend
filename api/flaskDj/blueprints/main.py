from flask import Blueprint, current_app

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return "Hello, World!"
