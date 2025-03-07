from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Email, Optional, URL
from app.models import SOCIAL_LINKS


class ProfileFormBasic(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Description', validators=[Optional()])
    
    submit = SubmitField('Save')


class ProfileFormSocial(FlaskForm):
    link_fields = {}
    for field_name, label in SOCIAL_LINKS.items():
        link_fields[field_name] = URLField(label, validators=[Optional(), URL()])
    
    locals().update(link_fields)

    submit = SubmitField('Save')