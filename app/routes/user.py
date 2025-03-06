from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models import User, Profile
from app.forms import ProfileForm

user = Blueprint('user', __name__)

@login_required
@user.route('/profile/<int:user_id>')
def profile(user_id):
    user_data = User.query.get_or_404(user_id)
    return render_template('user/profile.html', title='Profile', user=user_data)


@login_required
@user.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()

    user_data = User.query.filter_by(id=current_user.id).first()
    profile_data = Profile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        form.username.data = user_data.username
        form.email.data = user_data.email

        if profile_data:
            form.description.data = profile_data.description

    if form.validate_on_submit():
        if user_data:
            user_data.username = form.username.data
            user_data.email = form.email.data

        if profile_data:
            profile_data.description = form.description.data
        else:
            new_profile = Profile(
                description=form.description.data,
                user_id=current_user.id
            )

            db.session.add(new_profile)
            db.session.commit()

        db.session.commit()

        return redirect(url_for('user.profile', user_id=current_user.id))

    return render_template('user/edit_profile.html', form=form)