import datetime
import sqlalchemy
import flask_login
import werkzeug.security
from .. import db
from .. import utils
from .. import errors
from .mixins import ModelMixin

class UserError(errors.DataError):
    """User model data error.
    """
    pass


class User(db.Base, ModelMixin, flask_login.UserMixin):
    """Model defining system users.

    username: Username.
    display_name: Name shown in all UIs when referencing the user.
    email: Email.
    password: Password hash and salt.
    reset_password: Boolean whether the user will be forced to reset their password on next login.
    date_added: Date and time user was added to the database.
    security_token: Password first time creation and reset tokens (sent to the user by email).
    tokey_expiry: Date and time security_token expires.
    """
    __tablename__ = 'users'

    # Attributes
    username = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    display_name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(200))  # Nullable to allow email prompted registration
    reset_password = sqlalchemy.Column(sqlalchemy.Boolean)  # Force password reset on next login if True
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    security_token = sqlalchemy.Column(sqlalchemy.String(100))
    token_expiry = sqlalchemy.Column(sqlalchemy.DateTime)

    # Relationships
    groups_created = sqlalchemy.orm.relationship('Group', foreign_keys='Group.added_by', backref='added_user')
    groups_modified = sqlalchemy.orm.relationship('Group', foreign_keys='Group.modified_by', backref='modified_user')
    webhooks = sqlalchemy.orm.relationship('Webhook', backref='added_user')
    settings = sqlalchemy.orm.relationship('Setting', backref='modified_user')

    def __init__(self,
                 username=None,
                 display_name=None,
                 email=None,
                 password=None,
                 reset_password=None,
                 date_added=None,
                 security_token=None,
                 token_expiry=None):
        super()
        self.username = username
        self.display_name = display_name
        self.email = email
        self.password = password
        self.reset_password = reset_password
        self.date_added = date_added
        self.security_token = security_token
        self.token_expiry = token_expiry

    @property
    def id(self):
        """Used by flask_login to identify a user, returns username.
        """
        return self.username

    @property
    def self(self):
        """Get true self, workaround for proxied user objects (like with flask_login.current_user).
        """
        return self

    def set_password(self, passwd):
        """Set password for user (inc. database update).
        """
        self.password = self.gen_password(passwd)
        db.session.commit()

    def check_password(self, passwd):
        """Checks given password is valid.

        :param passwd: Password to check
        :return: True if valid else False
        """
        return werkzeug.security.check_password_hash(self.password, passwd)

    @classmethod
    def add_and_notify(cls, username, display_name, email, password=None, reset_password=None):
        """Create user, add to database and notify user of account creation via email.
        """
        security_token = None
        if not password:
            reset_password = True
            security_token = utils.gen_token()
        user = cls.add(username, display_name, email, password, reset_password, security_token)
        #TODO send welcome email (inculding token if no password set)
        return user

    @classmethod
    def add(cls, username, display_name, email, password=None, reset_password=None, security_token=None):
        """Create user and add to database.
        """
        if cls.get(username):
            raise UserError('User already exists.')
        if password:
            password = cls.gen_password(password)
        now = datetime.datetime.now()
        if not security_token:
            user = cls(username, display_name, email, password, reset_password, now)
        else:
            token_expiry = now + datetime.timedelta(hours=24)  #TODO move hours to database setting
            user = cls(username, display_name, email, password, reset_password, now, security_token, token_expiry)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get(cls, username):
        """Get User by username.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def check_login(cls, username, passwd):
        """Checks if a given username/password pair is value.

        :return: User if valid, else False
        """
        user = cls.get(username)
        if user and user.check_password(passwd):
            return user
        return False

    @classmethod
    def gen_password(cls, passwd):
        """Generate password hash from password.
        """
        return werkzeug.security.generate_password_hash(passwd)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
