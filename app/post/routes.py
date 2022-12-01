from flask import redirect, flash, url_for
from flask_login import current_user, login_required
from ..models import Post
from .. import db
from . import bp


@bp.route('/deletepost/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post and post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('post deleted')
    return redirect(url_for('main.index'))
    

