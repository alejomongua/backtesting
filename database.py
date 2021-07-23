import sqlite3

DATABASE_NAME = 'database.sqlite3'


class Database():
    class __Database:
        def __init__(self):
            conn = sqlite3.connect(DATABASE_NAME)
            self.cur = conn.cursor()

        def execute(self, query: str):
            self.cur.execute(query)

        def fetchone(self, query: str):
            self.cur.fetchone(query)

    instance = None

    def __init__(self):
        if not Database.instance:
            Database.instance = Database.__Database()

    def __getattr__(self, name):
        return getattr(self.instance, name)
