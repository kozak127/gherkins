from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SettingsForm(Form):
    cal_delimiter = StringField('cal_delimiter', validators=[DataRequired(), Length(min=1, max=10)])
    cal_url = StringField('cal_url', validators=[DataRequired()])
    cal_groups = StringField('cal_groups', validators=[DataRequired()])
    sum_task_delimiter = StringField('sum_task_delimiter', validators=[DataRequired(), Length(min=1, max=10)])

    def get_values_from_model(self, settings):
        self.cal_delimiter.data = settings.cal_delimiter
        self.cal_url.data = settings.cal_url
        self.cal_groups.data = settings.cal_groups
        self.sum_task_delimiter.data = settings.sum_task_delimiter
