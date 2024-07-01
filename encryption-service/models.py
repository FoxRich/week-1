from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(10), unique=True, nullable=False)
    secret = db.Column(db.String(10), nullable=False)
    sessions = db.relationship('Session', back_populates='user')

class Method(db.Model):
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(50), nullable=False)
    json_params = db.Column(db.JSON, nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'), nullable=False)
    data_in = db.Column(db.Text, nullable=False)
    data_out = db.Column(db.Text, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_op = db.Column(db.Float, nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', back_populates='sessions')
    method = db.relationship('Method')
