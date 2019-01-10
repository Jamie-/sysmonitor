import flask_wtf
import wtforms
import wtforms.validators as validators


class AddForm(flask_wtf.FlaskForm):
    slug = wtforms.StringField('slug', validators=[validators.DataRequired(), validators.Length(min=2, max=30), validators.Regexp('^(?:[a-zA-Z]|\d|-|_|\.)+$', message='Slug contains invalid characters.')])
    name = wtforms.StringField('name', validators=[validators.DataRequired(), validators.Length(min=2, max=30)])
    url = wtforms.StringField('url', validators=[validators.DataRequired(), validators.Regexp('^https?://.+', message='URL must begin http:// or https://')])
    verify = wtforms.BooleanField('verify')
    submit = wtforms.SubmitField('Add')


class DeleteForm(flask_wtf.FlaskForm):
    slug = wtforms.HiddenField('slug')
    delete = wtforms.SubmitField('Delete')
