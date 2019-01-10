import flask
import flask_login
import ui.forms.auth
from core.model.user import User

auth = flask.Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def route_login():
    form = ui.forms.auth.LoginForm()
    if form.validate_on_submit():
        user = User.check_login(form.username.data, form.password.data)
        if user:
            flask_login.login_user(user)
            flask.flash('Logged in successfully.', 'success')

            next = flask.request.args.get('next')
            return flask.redirect('/admin')  #TODO update to use `next` (but must be filtered correctly)
        flask.flash('Invalid username/password.', 'danger')
    return flask.render_template('auth/login.html', form=form)


@auth.route('/logout')
@flask_login.login_required
def route_logout():
    flask_login.logout_user()
    return flask.redirect('/')
