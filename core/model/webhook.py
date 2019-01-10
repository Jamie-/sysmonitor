import datetime
import sqlalchemy
import flask_login
from .. import db
from .. import errors
from .mixins import ModelMixin, SlugMixin
from .user import User

class WebhookError(errors.DataError):
    """Webhook model data error.
    """
    pass


class Webhook(db.Base, ModelMixin, SlugMixin):
    """Model defining multipurpose webhooks.

    slug: String uniquely identifying webhook.
    name: Webhook name.
    url: URL to be requested.
    verify: Whether to force certificate checking if URL uses SSL.
    date_added: Date and time webhook was added to the database.
    added_by: Username of the user who added the webhook.

    Class also has property added_user created by the foreign key back reference to the respective User object.
    """
    __tablename__ = 'webhooks'

    # Attributes
    slug = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)
    verify = sqlalchemy.Column(sqlalchemy.Boolean)  # Fail if URL is not https or cert is invalid
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    added_by = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey('users.username'))

    def __init__(self,
                 slug=None,
                 name=None,
                 url=None,
                 verify=None,
                 date_added=None,
                 added_by=None):
        super()
        self.slug = slug
        self.name = name
        self.url = url
        self.verify = verify
        self.date_added = date_added
        self.added_by = added_by

    def is_secure(self):
        """Determine if the URL uses SSL.
        """
        return self.url.startswith('https')

    @classmethod
    def add(cls, slug, name, url, verify=False, added_by=None):
        """Create Webhook object and add to database.
        """
        if cls.get(slug):
            raise WebhookError('Webhook slug already exists.')
        now = datetime.datetime.now()
        added_by_username = None
        if added_by:
            if not isinstance(added_by, User):
                raise TypeError('Expected instance of User not {}.'.format(type(added_by)))
            added_by_username = added_by.username
        webhook = cls(slug, name, url, verify, now, added_by_username)
        db.session.add(webhook)
        db.session.commit()
        return webhook

    def __repr__(self):
        return "<Webhook '{}'>".format(self.slug)
