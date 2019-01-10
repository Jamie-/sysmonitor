import flask_wtf
import wtforms
import wtforms.validators as validators


class AddForm(flask_wtf.FlaskForm):
    slug = wtforms.StringField('slug', validators=[validators.DataRequired(), validators.Length(min=2, max=30), validators.Regexp('^(?:[a-zA-Z]|\d|-|_|\.)+$', message='Slug contains invalid characters.')])
    name = wtforms.StringField('name', validators=[validators.DataRequired(), validators.Length(min=2, max=30)])
    color = wtforms.StringField('color', validators=[validators.Optional(), validators.Regexp('^[A-Fa-f0-9]{6}$', message='Not a valid hex color code.')])
    submit = wtforms.SubmitField('Add')


class EditForm(flask_wtf.FlaskForm):
    slug = wtforms.HiddenField('slug')
    name = wtforms.StringField('name', validators=[validators.DataRequired(), validators.Length(min=2, max=30)])
    color = wtforms.StringField('color', validators=[validators.Optional(), validators.Regexp('^[A-Fa-f0-9]{6}$', message='Not a valid hex color code.')])
    submit = wtforms.SubmitField('Save')


class DeleteForm(flask_wtf.FlaskForm):
    slug = wtforms.HiddenField('slug')
    delete = wtforms.SubmitField('Delete')
