from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    settings = db.relationship('Settings', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.nickname


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    cal_delimiter = db.Column(db.String(10))
    cal_name = db.Column(db.String(250))
    sum_task_delimiter = db.Column(db.String(10))
    csv_delimiter = db.Column(db.String(10))
    csv_divide_weeks = db.Column(db.Boolean)

    def get_values_from_form(self, form):
        self.cal_delimiter = form.cal_delimiter.data
        self.cal_name = form.cal_name.data
        self.sum_task_delimiter = form.sum_task_delimiter.data
        self.csv_delimiter = form.csv_delimiter.data
        self.csv_divide_weeks = form.csv_divide_weeks.data


class Task():

    def __init__(self, project, summary, date, duration):
        self.project = project
        self.summary = summary
        self.date = date
        self.duration = duration

    def is_in_group(self, group):
        for project in group:
            if self.project == project:
                return True
        return False


class TaskManager():

    def __init__(self):
        self.tasks = []

    def get_tasks_for_group(self, group):
        to_return = []
        for task in self.tasks:
            if task.is_in_group(group):
                to_return.append(task)
        return to_return

    def get_tasks_for_group(self, group, date):
        to_return = []
        for task in self.tasks:
            if task.date == date and task.is_in_group(group):
                to_return.append(task)
        return to_return

    def get_tasks_for_group(self, group, date_start, date_end):
        to_return = []
        for task in self.tasks:
            if date_start <= task.date <= date_end and task.is_in_group(group):
                to_return.append(task)
        return to_return