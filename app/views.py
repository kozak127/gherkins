from datetime import datetime
from app.oauth import OAuthSignIn
from app.report import DailyReport, WeeklyReport, MonthlyReport
from app.task import TaskManager
from flask import render_template, flash, redirect, session, url_for, request, g, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, SettingsForm
from app.models import User, Settings


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    settings_instance = g.user.settings.first()
    if form.validate_on_submit():
        if settings_instance is None:
            settings_instance = Settings()
        settings_instance.set_values_from_settings_form(form)
        settings_instance.User = g.user
        db.session.add(settings_instance)
        db.session.commit()
        flash('Settings saved!')
        return redirect(url_for('index'))
    if settings_instance is not None:
        form.set_values_from_settings_model(settings_instance)
    return render_template('settings.html', form=form)


@app.route('/generate/csv/daily')
@login_required
def generate_csv_daily():
    settings_instance = g.user.settings.first()
    if settings_instance is None:
        flash("You don't have any saved settings")
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    try:
        task_manager = TaskManager(url, cal_delimiter)
    except ValueError:
        flash("URL to ical file is invalid")
        return redirect(url_for('settings'))

    date_start = datetime.strptime('01022015', "%d%m%Y").date()
    date_end = datetime.strptime('28022015', "%d%m%Y").date()
    report = DailyReport(groups, task_manager, sum_task_delimiter, date_start, date_end)
    response = make_response(report.to_csv_string())
    response.headers["Content-Disposition"] = "attachment; filename=daily.csv"
    return response


@app.route('/generate/csv/weekly')
@login_required
def generate_csv_weekly():
    settings_instance = g.user.settings.first()
    if settings_instance is None:
        flash("You don't have any saved settings")
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    try:
        task_manager = TaskManager(url, cal_delimiter)
    except ValueError:
        flash("URL to ical file is invalid")
        return redirect(url_for('settings'))

    date_start = datetime.strptime('01022015', "%d%m%Y").date()
    date_end = datetime.strptime('28022015', "%d%m%Y").date()
    report = WeeklyReport(groups, task_manager, sum_task_delimiter, date_start, date_end)
    response = make_response(report.to_csv_string())
    response.headers["Content-Disposition"] = "attachment; filename=weekly.csv"
    return response


@app.route('/generate/csv/monthly')
@login_required
def generate_csv_monthly():
    settings_instance = g.user.settings.first()
    if settings_instance is None:
        flash("You don't have any saved settings")
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    try:
        task_manager = TaskManager(url, cal_delimiter)
    except ValueError:
        flash("URL to ical file is invalid")
        return redirect(url_for('settings'))

    date_start = datetime.strptime('01022015', "%d%m%Y").date()
    date_end = datetime.strptime('28022015', "%d%m%Y").date()
    report = MonthlyReport(groups, task_manager, sum_task_delimiter, date_start, date_end)
    response = make_response(report.to_csv_string())
    response.headers["Content-Disposition"] = "attachment; filename=monthly.csv"
    return response
