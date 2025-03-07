from flask import (Blueprint, render_template, redirect, url_for, 
                   request, flash, current_app)
from flask_login import login_required, current_user

from app.extensions import db
from app.models import User, Profile, SOCIAL_LINKS
from app.forms.user_forms import ProfileFormBasic, ProfileFormSocial

user_bp = Blueprint('user', __name__)

def get_user_social_links(profile_data):
    social_links = {
        field_name: getattr(profile_data, field_name, None) 
        for field_name in SOCIAL_LINKS.keys()
    }
    return social_links


@login_required
@user_bp.route('/profile/<int:user_id>')
def profile(user_id):
    user_data = User.query.get_or_404(user_id)
    social_links = get_user_social_links(user_data.profile)

    return render_template('user/profile.html', title='Profile', 
                            user=user_data, SOCIAL_LINKS=SOCIAL_LINKS, social_links=social_links)


@login_required
@user_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileFormBasic()

    user_data = User.query.filter_by(id=current_user.id).first()
    profile_data = user_data.profile

    if request.method == 'GET':
        try:
            form.username.data = user_data.username
            form.email.data = user_data.email
            form.description.data = profile_data.description if profile_data else ""
        
        except Exception as e:
            flash("Произошла ошибка при загрузке данных. Попробуйте снова.", "error")
            current_app.logger.error(f"Error during profile data loading: {e}")
            return redirect(url_for('user.profile', user_id=current_user.id))

    if form.validate_on_submit():
        try:
            changes_made = False

            if user_data.username != form.username.data:
                user_data.username = form.username.data
                changes_made = True

            if user_data.email != form.email.data:
                user_data.email = form.email.data
                changes_made = True

            if profile_data:
                if profile_data.description != form.description.data:
                    profile_data.description = form.description.data
                    changes_made = True

            if changes_made:
                db.session.commit()
                flash("Изменения успешно сохранены.", "success")

            return redirect(url_for('user.profile', user_id=current_user.id))

        except Exception as e:
            flash("Произошла ошибка при сохранении данных. Попробуйте снова.", "error")
            current_app.logger.error(f"Error during profile data saving: {e}")
            return redirect(url_for('user.edit_profile'))

    return render_template('user/edit_profile.html', title='Edit Profile',
                            form=form, SOCIAL_LINKS=SOCIAL_LINKS, user=user_data)


@login_required
@user_bp.route('/profile/edit/social_links', methods=['GET', 'POST'])
def edit_social_links():
    form = ProfileFormSocial()

    profile_data = Profile.query.filter_by(user_id=current_user.id).first()
    social_links = get_user_social_links(profile_data)

    if request.method == 'GET':
        try:
            for field_name in SOCIAL_LINKS.keys():
                link_value = social_links.get(field_name, '')
                getattr(form, field_name).data = link_value

        except Exception as e:
            flash("Произошла ошибка при загрузке данных. Попробуйте снова.", "error")
            current_app.logger.error(f"Error during social links data loading: {e}")
            return redirect(url_for('user.profile', user_id=current_user.id))

    if form.validate_on_submit():
        try:
            changes_made = False
            
            for field_name in SOCIAL_LINKS.keys():
                current_value = getattr(profile_data, field_name)
                new_value = getattr(form, field_name).data or None

                if current_value != new_value:
                    setattr(profile_data, field_name, new_value)
                    changes_made = True

            if changes_made:
                db.session.commit()
                flash("Социальные ссылки успешно обновлены.", "success")
        
            return redirect(url_for('user.profile', user_id=current_user.id))

        except Exception as e:
            flash("Произошла ошибка при сохранении данных. Попробуйте снова.", "error")
            current_app.logger.error(f"Error during saving social links: {e}")
            return redirect(url_for('user.social_links'))

    return render_template('user/edit_social_links.html', title='Edit Social Links',
                           form=form, social_links=social_links, SOCIAL_LINKS=SOCIAL_LINKS)