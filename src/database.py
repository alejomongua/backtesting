from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'database.sqlite3'
CONNECTION_STRING = f"sqlite:///{DATABASE_NAME}"


class Database():
    class __Database:
        def __init__(self):
            self.engine = create_engine(CONNECTION_STRING)

        def drop_database(self, Base):
            Base.metadata.drop_all(self.engine)

        def create_database(self, Base):
            Base.metadata.create_all(self.engine)

        def persist(self, model):
            DBSession = sessionmaker(bind=self.engine)
            self.session = DBSession()
            self.session.add(model)
            self.session.commit()

    instance = None

    def __init__(self):
        if not Database.instance:
            Database.instance = Database.__Database()

    def __getattr__(self, name):
        return getattr(self.instance, name)
