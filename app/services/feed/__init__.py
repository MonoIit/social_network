from flask import Blueprint

feed_bp = Blueprint('feed_bp', __name__, template_folder='templates')

from . import routes