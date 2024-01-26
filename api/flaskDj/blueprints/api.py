from flask import Blueprint, Flask, current_app, jsonify, send_file
from flaskDj.service import DatabaseService

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/data", methods=["GET"])
def get_all_data():
    from flaskDj.models import Tracks

    try:
        # Query all data from the database
        all_data = Tracks.query.all()

        # Convert the SQLAlchemy objects to a list of dictionaries
        data_list = [item.to_dict() for item in all_data]
        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/audio/<path>", methods=["GET"])
def fetch_file(path: int):
    try:
        with current_app.app_context():
            track = current_app.db_service.get_track(track_id=path)
            return send_file(track.fileLocation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
