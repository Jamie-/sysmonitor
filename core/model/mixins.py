import datetime
from .. import db

class ModelMixin:
    """Helpful methods for database models.
    """

    def update(self, username=None):
        """Trigger a database update on self, marks modified_by as username given if self has modified_by attribute.
        """
        if hasattr(self, 'date_modified'):  # If object tracks modified times, update
            self.date_modified = datetime.datetime.now()
        if hasattr(self, 'modified_by') and username:
            self.modified_by = username
        db.session.commit()

    def delete(self):
        """Delete self from the database.
        """
        db.session.delete(self)
        db.session.commit()


class SlugMixin:
    """Helpful methods for database models that have a slug field.
    """

    @classmethod
    def get(cls, slug):
        """Get instance of model by slug.
        """
        return cls.query.filter_by(slug=slug).first()
