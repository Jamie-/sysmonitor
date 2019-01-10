import flask_wtf
import wtforms
import wtforms.fields.html5
import wtforms.validators as validators


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('username', validators=[validators.DataRequired()])
    password = wtforms.PasswordField('password', validators=[validators.DataRequired()])
