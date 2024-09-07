from flask import Blueprint

messanger_bp = Blueprint('messanger_bp', __name__, template_folder='templates')

from . import routes