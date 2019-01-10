import flask
import flask_login
import core.db
import core.utils
from core.model.user import User
from core.config import Config, CONFIG_FILE_PATH

from .views.dash import dash
from .views.auth import auth
from .views.admin import admin
from .views.api import api


# Parse config
config = Config.from_file(CONFIG_FILE_PATH)


# Initialise Flask & register blueprints
app = flask.Flask(__name__)
app.config.update(config.get_flask_config())

app.register_blueprint(dash)
app.register_blueprint(auth)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')


# Initialise login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.route_login'
login_manager.login_message = 'You need to login to do that.'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(username):
    return User.get(username)


# Add Jinja2 customs
app.jinja_env.globals['flask_login'] = flask_login
app.jinja_env.filters['prettydate'] = core.utils.pretty_date
app.jinja_env.filters['b64encode'] = core.utils.b64encode


# Nicely shut SQLAlchemy sessions
@app.teardown_appcontext
def shutdown_session(exception=None):
    core.db.session.remove()
