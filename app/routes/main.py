from flask import Blueprint, render_template

from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('main/index.html', title='Home', users=users)
