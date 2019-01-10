import flask
import flask_login
from core.model.user import User, UserError
from core.model.settings import Setting
from core.model.group import Group, GroupError
from core.model.webhook import Webhook, WebhookError
import ui.forms.admin.users
import ui.forms.admin.groups
import ui.forms.admin.webhooks

admin = flask.Blueprint('admin', __name__)


@admin.before_request
def before_request():
    if not flask_login.current_user.is_authenticated:
        return flask.current_app.login_manager.unauthorized()


@admin.route('/')
def route_index():
    return flask.redirect(flask.url_for('.route_status'))


@admin.route('/status')
def route_status():
    return flask.render_template('admin/status.html')


@admin.route('/services')
def route_services():
    return flask.render_template('admin/services.html')


@admin.route('/groups', methods=['GET', 'POST'])
def route_groups():
    add_form = ui.forms.admin.groups.AddForm(prefix='add')
    edit_form = ui.forms.admin.groups.EditForm(prefix='edit')
    delete_form = ui.forms.admin.groups.DeleteForm(prefix='delete')

    # Add group form
    if add_form.submit.data and add_form.validate_on_submit():
        try:
            # If color is specified and not white, set it
            color = None
            if add_form.color.data:
                color = add_form.color.data
                if color.lower() == 'fff' or color.lower() == 'ffffff':
                    color = None
            group = Group.add(
                add_form.slug.data,
                add_form.name.data,
                color=color,
                added_by=flask_login.current_user.self
            )
            flask.flash('Added group {} successfully.'.format(group.name), 'success')
            return flask.jsonify({'status': 'success'})
        except GroupError as e:
            add_form.slug.errors.append(str(e))
    if add_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': add_form.errors})

    # Edit group form
    if edit_form.submit.data and edit_form.validate_on_submit():
        group = Group.get(edit_form.slug.data)
        if group:
            group.name = edit_form.name.data
            group.color = edit_form.color.data
            group.update(username=flask_login.current_user.username)
            flask.flash('Saved changes to {}.'.format(group.name), 'success')
            return flask.jsonify({'status': 'success'})
        else:
            return flask.jsonify({'status': 'failed', 'reason': "That group doesn't exist"})
    if edit_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': edit_form.errors})

    # Delete group form
    if delete_form.delete.data and delete_form.validate_on_submit():
        group = Group.get(delete_form.slug.data)
        if group:
            group.delete()
            flask.flash('Deleted group {} successfully.'.format(group.name), 'success')
        else:
            flask.abort(400)

    return flask.render_template('admin/groups.html',
                                 add_form=add_form,
                                 edit_form=edit_form,
                                 delete_form=delete_form,
                                 groups=Group.query.all())


@admin.route('/webhooks', methods=['GET', 'POST'])
def route_webhooks():
    add_form = ui.forms.admin.webhooks.AddForm(prefix='add')
    delete_form = ui.forms.admin.webhooks.DeleteForm(prefix='delete')

    # Add webhook form
    if add_form.submit.data and add_form.validate_on_submit():
        try:
            webhook = Webhook.add(
                add_form.slug.data,
                add_form.name.data,
                add_form.url.data,
                add_form.verify.data,
                flask_login.current_user.self
            )
            flask.flash('Added webhook {} successfully.'.format(webhook.name), 'success')
            return flask.jsonify({'status': 'success'})
        except WebhookError as e:
            add_form.slug.errors.append(str(e))
    if add_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': add_form.errors})

    # Delete webhook form
    if delete_form.delete.data and delete_form.validate_on_submit():
        webhook = Webhook.get(delete_form.slug.data)
        if webhook:
            webhook.delete()
            flask.flash('Deleted webhook {} successfully.'.format(webhook.name), 'success')
        else:
            flask.abort(400)

    return flask.render_template('admin/webhooks.html',
                                 add_form=add_form,
                                 delete_form=delete_form,
                                 webhooks=Webhook.query.all())


@admin.route('/users', methods=['GET', 'POST'])
def route_users():
    add_form = ui.forms.admin.users.AddForm(prefix='add_user')
    edit_form = ui.forms.admin.users.EditForm(prefix='edit')
    reset_pw_form = ui.forms.admin.users.ResetPasswordForm(prefix='reset_pw')
    delete_form = ui.forms.admin.users.DeleteForm(prefix='delete_user')

    # Add user form
    if add_form.submit.data and add_form.validate_on_submit():
        try:
            user = User.add_and_notify(
                add_form.username.data,
                add_form.display_name.data,
                add_form.email.data,
                add_form.password.data,
                add_form.force_reset.data)
            flask.flash('Added user {} successfully.'.format(user.username), 'success')
            return flask.jsonify({'status': 'success'})
        except UserError as e:
            add_form.username.errors.append(str(e))
    if add_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': add_form.errors})

    # Edit user form
    if edit_form.submit.data and edit_form.validate_on_submit():
        user = User.get(edit_form.username.data)
        if user:
            user.display_name = edit_form.display_name.data
            user.email = edit_form.email.data
            if edit_form.force_reset.data:
                user.reset_password = True
            user.update()
            flask.flash('Saved changes to {}.'.format(user.username), 'success')
            return flask.jsonify({'status': 'success'})
        else:
            return flask.jsonify({'status': 'failed', 'reason': "That user doesn't exist"})
    if edit_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': edit_form.errors})

    # Reset password form
    if reset_pw_form.submit.data and reset_pw_form.validate_on_submit():
        print(reset_pw_form.username.data)
        user = User.get(reset_pw_form.username.data)
        if user:
            user.set_password(reset_pw_form.password.data)
            return flask.jsonify({'status': 'success'})
        else:
            return flask.jsonify({'status': 'failed', 'reason': "That user doesn't exist"})
    if reset_pw_form.submit.data:
        return flask.jsonify({'status': 'errors', 'errors': reset_pw_form.errors})

    # Delete user form
    if delete_form.delete.data and delete_form.validate_on_submit():
        user = User.get(delete_form.username.data)
        if user and user == flask_login.current_user:
            flask.flash("You can't delete your own user.", 'danger')
        elif user:
            user.delete()
            flask.flash('Deleted user {} successfully.'.format(user.username), 'success')
        else:
            flask.abort(400)

    return flask.render_template('admin/users.html',
                                 users=User.query.all(),
                                 add_form=add_form,
                                 edit_form=edit_form,
                                 reset_pw_form=reset_pw_form,
                                 delete_form=delete_form)


@admin.route('/settings')
def route_settings():
    return flask.render_template('admin/settings.html', settings=Setting.query.all())
