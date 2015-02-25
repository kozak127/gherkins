from datetime import datetime
from app.report import DailyReport, WeeklyReport, MonthlyReport
from app.task import TaskManager
from flask import render_template, flash, redirect, session, url_for, request, g, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app.forms import LoginForm, SettingsForm
from app.models import User


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
@login_required
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        settings_instance = g.user.settings.first()
        settings_instance.set_values_from_form(form)
        settings_instance.user = g.user
        db.session.add(settings_instance)
        db.session.commit()
        flash('Settings saved!')
        return redirect(url_for('index'))
    settings_instance = g.user.settings.first()
    if settings_instance is not None:
        form.get_values_from_model(settings_instance)
    return render_template('settings.html', form=form)


@app.route('/generate/csv/daily')
@login_required
def generate_csv_daily():
    settings_instance = g.user.settings.first()
    if settings_instance is None:
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    task_manager = TaskManager(url, cal_delimiter)
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
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    task_manager = TaskManager(url, cal_delimiter)
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
        return redirect(url_for('settings'))

    url = settings_instance.cal_url
    cal_delimiter = settings_instance.cal_delimiter
    sum_task_delimiter = settings_instance.sum_task_delimiter
    groups = settings_instance.get_list_of_groups()

    task_manager = TaskManager(url, cal_delimiter)
    date_start = datetime.strptime('01022015', "%d%m%Y").date()
    date_end = datetime.strptime('28022015', "%d%m%Y").date()
    report = MonthlyReport(groups, task_manager, sum_task_delimiter, date_start, date_end)
    response = make_response(report.to_csv_string())
    response.headers["Content-Disposition"] = "attachment; filename=monthly.csv"
    return response
