from app.oauth import OAuthSignIn
from flask import render_template, flash, redirect, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import SettingsForm, EventForm
from app.models import User, Settings, Event


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


@app.route('/settings')
@login_required
def settings():
    form = SettingsForm()
    settings_instance = g.user.settings.first()
    if form.validate_on_submit():
        if settings_instance is None:
            settings_instance = Settings()
        settings_instance.set_from_dict_form(form.__dict__)
        settings_instance.User = g.user
        db.session.add(settings_instance)
        db.session.commit()
        flash('Settings saved')
        return redirect(url_for('index'))
    if settings_instance is not None:
        form.set_from_dict_model(settings_instance.__dict__)
    return render_template('settings.html', form=form)


@app.route('/event')
def events():
    return redirect(url_for('event_list'))


@app.route('/event/list', methods=['GET', 'POST'])
def event_list():
    events = Event.query.all()
    return render_template('events/list.html', events=events)


@app.route('/event/show/<id>')
def event_show(id):
    if id is not None:
        form = EventForm()
        event_instance = Event.query.filter_by(id=id).first()
        form.set_from_dict_model(event_instance.__dict__)
        return render_template('event/show.html', form=form)
    else:
        flash('Unable to find event')
        return redirect(url_for('event_list'))


@app.route('event/create')
def event_create():
    return event_edit(None)


@app.route('/event/edit/<id>')
def event_edit(id):
    form = EventForm()
    event_instance = Event()
    if id is not None:
        event_instance = Event.query.filter_by(id=id).first()
    if form.validate_on_submit():
        event_instance.set_from_dict_form(form.__dict__)
        if id is None:
            event_instance.creator = g.user
        db.session.add(event_instance)
        db.session.commit()
        flash('Event saved')
        return redirect(url_for('event_list'))
    if event_instance is not None:
        form.set_from_dict_model(event_instance.__dict__)
    render_template('event/edit.html', form=form)


@app.route('/event/delete/<id>')
def event_delete(id):
    if id is not None:
        event = Event.query.filter_by(id=id).first()
        event.status = 'deleted'
        flash('Event deleted')
        return redirect(url_for('event_list'))
    else:
        flash('Unable to find event')
        return redirect(url_for('event_list'))
