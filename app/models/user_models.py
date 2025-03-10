from app.extensions import db
from flask_login import UserMixin

SOCIAL_LINKS = {
    'github': 'GitHub',
    'behance': 'Behance',
    'youtube': 'YouTube',
    'personal_website': 'Personal Website',
    'telegram': 'Telegram',
    'vk': 'VK'
}

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    profile = db.relationship('Profile', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    github = db.Column(db.String(255), nullable=True)
    behance = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.String(255), nullable=True)
    personal_website = db.Column(db.String(255), nullable=True)
    telegram = db.Column(db.String(255), nullable=True)
    vk = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f'<Profile {self.id} for user {self.user.username}>'