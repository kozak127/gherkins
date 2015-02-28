from app import db
from flask.ext.login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    settings = db.relationship('Settings', backref='User', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    cal_delimiter = db.Column(db.String(10))
    cal_url = db.Column(db.String(250))
    cal_groups = db.Column(db.String(250))
    sum_task_delimiter = db.Column(db.String(10))

    def set_values_from_form(self, form):
        self.cal_delimiter = form.cal_delimiter.data
        self.cal_url = form.cal_url.data
        self.cal_groups = form.cal_groups.data
        self.sum_task_delimiter = form.sum_task_delimiter.data

    def get_list_of_groups(self):
        return self.cal_groups.split('#')
