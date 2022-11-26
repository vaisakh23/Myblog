from flask import render_template
from .. import db
from . import bp

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page not found'), 404

@bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title='Internal server error'), 500
