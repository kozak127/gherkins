from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)  # python 2

    def __repr__(self):
        return '<User %r>' % self.nickname


class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', lazy='dynamic')

    cal_delimiter = db.Column(db.String(10))
    sum_task_delimiter = db.Column(db.String(10))
    csv_delimiter = db.Column(db.String(10))
    csv_divide_weeks = db.Column(db.Integer)