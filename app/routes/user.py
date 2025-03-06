from flask import Blueprint, render_template
from flask_login import login_required

from app.models import User

user = Blueprint('user', __name__)

@login_required
@user.route('/profile/<int:user_id>')
def profile(user_id):
    user_data = User.query.get_or_404(user_id)
    return render_template('user/profile.html', title='Profile', user=user_data)
