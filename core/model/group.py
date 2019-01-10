import datetime
import sqlalchemy
import flask_login
from .. import db
from .. import errors
from .mixins import ModelMixin, SlugMixin
from .user import User

class GroupError(errors.DataError):
    """Group model data error.
    """
    pass


class Group(db.Base, ModelMixin, SlugMixin):
    """Model defining service groups.

    Many services may be added to a group, however each service may only be part of one group.
    A group has a name and may have an icon and a colour assigned to it along with tracking metadata.

    slug: String uniquely identifying group.
    name: Group name.
    icon: Group icon (optional).
    color: Group colour (optional).
    date_added: Date and time group was added to the database.
    added_by: Username of the user who added the group.
    date_modified: Date and time group was last modified.
    modified_by: Username of the user who last modified the group.

    Class also has properties added_user and modified_user created by the foreign key back references to the respective User objects.
    """
    __tablename__ = 'groups'

    # Attributes
    slug = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.String(50))
    color = sqlalchemy.Column(sqlalchemy.String(6))
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    added_by = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey('users.username'))
    date_modified = sqlalchemy.Column(sqlalchemy.DateTime)
    modified_by = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey('users.username'))

    def __init__(self,
                 slug=None,
                 name=None,
                 icon=None,
                 color=None,
                 date_added=None,
                 added_by=None,
                 date_modified=None,
                 modified_by=None):
        super()
        self.slug = slug
        self.name = name
        self.icon = icon
        self.color = color
        self.date_added = date_added
        self.added_by = added_by
        self.date_modified = date_modified
        self.modified_by = modified_by

    @classmethod
    def add(cls, slug, name, icon=None, color=None, added_by=None):
        """Create Group object and add to database.
        """
        if cls.get(slug):
            raise GroupError('Group slug already exists.')
        now = datetime.datetime.now()
        added_by_username = None
        if added_by:
            if not isinstance(added_by, User):
                raise TypeError('Expected instance of User not {}.'.format(type(added_by)))
            added_by_username = added_by.username
        group = cls(slug, name, icon, color, now, added_by_username)
        db.session.add(group)
        db.session.commit()
        return group

    def __repr__(self):
        return "<Group '{}'>".format(self.slug)
