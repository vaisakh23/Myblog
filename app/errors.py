from flask import render_template
from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html', title='Internal server error'), 500
