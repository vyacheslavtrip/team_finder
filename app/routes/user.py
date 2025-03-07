from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models import User, Profile, SOCIAL_LINKS
from app.forms import ProfileForm

user = Blueprint('user', __name__)

@login_required
@user.route('/profile/<int:user_id>')
def profile(user_id):
    user_data = User.query.get_or_404(user_id)

    profile_data = Profile.query.filter_by(user_id=user_id).first()
    
    social_links = {}
    if profile_data:
        for field_name, label in SOCIAL_LINKS.items():
            social_links[field_name] = getattr(profile_data, field_name, None)

    return render_template('user/profile.html', title='Profile', user=user_data, SOCIAL_LINKS=SOCIAL_LINKS, social_links=social_links)


@login_required
@user.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()

    user_data = User.query.filter_by(id=current_user.id).first()
    profile_data = Profile.query.filter_by(user_id=current_user.id).first()

    social_links_data = {}

    if request.method == 'GET':
        form.username.data = user_data.username
        form.email.data = user_data.email

        if profile_data:
            form.description.data = profile_data.description

            # Собираем социальные ссылки в словарь
            for field_name in SOCIAL_LINKS.keys():
                link_value = getattr(profile_data, field_name, '')
                social_links_data[field_name] = link_value  # Если нет значения, передаем пустую строку
                getattr(form, field_name).data = link_value

    if form.validate_on_submit():
        if user_data:
            user_data.username = form.username.data
            user_data.email = form.email.data

        if profile_data:
            profile_data.description = form.description.data

            for field_name in SOCIAL_LINKS.keys():
                setattr(profile_data, field_name, getattr(form, field_name).data)
        else:
            new_profile = Profile(
                description=form.description.data,
                user_id=current_user.id,
                **{field_name: getattr(form, field_name).data for field_name in SOCIAL_LINKS.keys()}
            )

            db.session.add(new_profile)

        db.session.commit()

        return redirect(url_for('user.profile', user_id=current_user.id))

    return render_template('user/edit_profile.html', form=form, social_links_data=social_links_data, SOCIAL_LINKS=SOCIAL_LINKS, user=user_data)
