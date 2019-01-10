import sqlalchemy
import datetime
from .. import db
from .. import errors
from .mixins import ModelMixin
from .user import User


class SettingError(errors.DataError):
    """Setting model data error.
    """
    pass


class Setting(db.Base, ModelMixin):
    """Model defining application settings.

    key: Key
    value: Value
    date_modified: Date and time setting was last modified (or created).
    modified_by: Username of the user who last modified (or created) the setting.

    Class also has property modified_user created by the foreign key back reference to the respective User object.
    """
    __tablename__ = 'settings'

    key = sqlalchemy.Column(sqlalchemy.String(100), primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.String(200))
    date_modified = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    modified_by = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey('users.username'))

    def __init__(self,
                 key=None,
                 value=None,
                 date_modified=None,
                 modified_by=None):
        super()
        self.key = key
        self.value = value
        self.date_modified = date_modified
        self.modified_by = modified_by

    @classmethod
    def get(cls, key):
        """Get Setting by key.
        """
        return cls.query.filter_by(key=key).first()

    @classmethod
    def add(cls, key, value, modified_by=None):
        """Create a Setting object and add to database.

        modified_by should be a User object if add triggered by a user.
        """
        modified_by_username = None
        if modified_by:
            if not isinstance(modified_by, User):
                raise TypeError('Expected instance of User not {}.'.format(type(modified_by)))
            modified_by_username = modified_by.username
        setting = cls(key, value, datetime.datetime.now(), modified_by_username)
        db.session.add(setting)
        db.session.commit()
        return setting

    def __repr__(self):
        return "<Setting '{}'>".format(self.key)
