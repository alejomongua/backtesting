from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'database.sqlite3'
CONNECTION_STRING = f"sqlite:///{DATABASE_NAME}"


class Database():
    class __Database:
        def __init__(self):
            self.engine = create_engine(CONNECTION_STRING)

        def drop_model(self, Model):
            Model.metadata.drop_all(self.engine)

        def create_model(self, Model):
            Model.metadata.create_all(self.engine)

        def persist(self, items):
            DBSession = sessionmaker(bind=self.engine)
            self.session = DBSession()
            if hasattr(items, '__iter__'):
                for item in items:
                    self.session.add(item)
            else:
                self.session.add(items)
            self.session.commit()

        def get_session(self):
            DBSession = sessionmaker(bind=self.engine)
            return DBSession()

    instance = None

    def __init__(self):
        if not Database.instance:
            Database.instance = Database.__Database()

    def __getattr__(self, name):
        return getattr(self.instance, name)
