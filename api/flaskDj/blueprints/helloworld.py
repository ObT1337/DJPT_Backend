from flask import Blueprint, current_app,jsonify
from flaskDj.service import DatabaseService
import time

bp = Blueprint('hw', __name__, url_prefix='/dummy')
@bp.route('/time')
def get_current_time():
    return jsonify({'time': time.time()})