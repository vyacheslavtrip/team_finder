from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Length, DataRequired, Email

class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(max=150)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email(), Length(max=150)])
    description = TextAreaField('Описание', validators=[Length(max=500)])
    submit = SubmitField('Сохранить')
