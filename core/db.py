import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from .config import Config, CONFIG_FILE_PATH

# Get database config
cfg = Config.from_file(CONFIG_FILE_PATH)['db']
db_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(cfg['username'], cfg['password'], cfg['host'], cfg['port'], cfg['db'])

engine = sqlalchemy.create_engine(db_url, pool_recycle=3600)
session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))

Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = session.query_property()


def init_db():
    """Create all database tables.

    Import all models that need creating so they are registered for the create_all()
    """
    from .model import user
    from .model import settings
    from .model import group
    from .model import webhook
    Base.metadata.create_all(bind=engine)
