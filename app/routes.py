from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.db.PostgresDB import PostgresDB
from .tools.tools import menu, side_menu

bp = Blueprint('main', __name__)


dbase = PostgresDB()



@bp.route('/')
@login_required
def index():
    return redirect(url_for('feed_bp.feed'))


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', menu=menu, side_menu=side_menu, current_user=current_user)
















