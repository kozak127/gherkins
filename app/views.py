from app.oauth import OAuthSignIn
from flask import render_template, flash, redirect, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import SettingsForm
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
