import flask_wtf
import wtforms
import wtforms.validators as validators


class AddForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('username', validators=[validators.DataRequired(), validators.Length(min=2, max=20), validators.Regexp('^(?:[a-zA-Z]|\d|-|_|\.)+$', message='Username contains invalid characters.')])
    display_name = wtforms.StringField('display_name', validators=[validators.DataRequired(), validators.Length(min=2, max=40)])
    email = wtforms.fields.html5.EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = wtforms.PasswordField('password', validators=[validators.Optional(), validators.Length(min=8)])
    force_reset = wtforms.BooleanField('force_reset')
    submit = wtforms.SubmitField('Add')


class EditForm(flask_wtf.FlaskForm):
    username = wtforms.HiddenField('username')
    display_name = wtforms.StringField('display_name', validators=[validators.DataRequired(), validators.Length(min=2, max=40)])
    email = wtforms.fields.html5.EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    force_reset = wtforms.BooleanField('force_reset')
    submit = wtforms.SubmitField('Save')


class ResetPasswordForm(flask_wtf.FlaskForm):
    username = wtforms.HiddenField('username')
    password = wtforms.PasswordField('new_password', validators=[validators.DataRequired(), validators.Length(min=8)])
    force_reset = wtforms.BooleanField('force_reset')
    submit = wtforms.SubmitField('Change')


class DeleteForm(flask_wtf.FlaskForm):
    username = wtforms.HiddenField('username')
    delete = wtforms.SubmitField('Delete')
