from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, read_only
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SettingsForm(Form):

    def set_from_dict_model(self, dict):
        raise NotImplementedError('Not implemented!')


class EventForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=6)])
    description = StringField('description', validators=[DataRequired()])
    start_date = DateField('start date', validators=[DataRequired()])
    #start_time = TimeField('start time', validators=[DataRequired()])
    end_date = DateField('end date', validators=[DataRequired()])
    #end_time = TimeField('end time', validators=[DataRequired()])
    creation_date = DateField('creation date')
    creator = StringField('creator')
    status = StringField('status', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        read_only(self.creator)
        read_only(self.creation_date)

    def set_from_dict_model(self, dict):
        self.name = dict["name"]
        self.description = dict["description"]
        self.start_date = dict["start_date"]
        self.end_date = dict["end_date"]
        self.creation_date = dict["creation_date"]
        self.creator = dict["creator"]
        self.status = dict["status"]
