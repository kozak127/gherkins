from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SettingsForm(Form):
    cal_delimiter = StringField('cal_delimiter', validators=[DataRequired(), Length(min=1, max=10)])
    cal_name = StringField('cal_name', validators=[DataRequired()])
    sum_task_delimiter = StringField('sum_task_delimiter', validators=[DataRequired(), Length(min=1, max=10)])
    csv_delimiter = StringField('csv_delimiter', validators=[DataRequired(), Length(min=1, max=1)])
    csv_divide_weeks = BooleanField('csv_divide_weeks', validators=[DataRequired()])

    def get_values_from_model(self, settings):
        self.cal_delimiter.data = settings.cal_delimiter
        self.cal_name.data = settings.cal_name
        self.sum_task_delimiter.data = settings.sum_task_delimiter
        self.csv_delimiter.data = settings.csv_delimiter
        self.csv_divide_weeks.data = settings.csv_divide_weeks
