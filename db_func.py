# coding=utf-8
import models

from os.path import join, isfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_FILE_PATH = join('.', 'sql.db')


class DB(object):
    def __init__(self):
        self.engine = self._make_connection()
        self.session = self._get_session(self.engine)

    def _make_connection(self):
        return create_engine('sqlite:///' + SQLITE_FILE_PATH)

    def _get_session(self, engine):
        DBSession = sessionmaker(bind=engine)
        return DBSession()

    def generate_db(self, base):
        base.metadata.create_all(self.engine)

    def add(self, transaction):
        self.session.add(transaction)
        self.session.commit()


db = DB()


def init_db():
    if not isfile(SQLITE_FILE_PATH):
        print('[ init DB ]')
        create_db()


def create_db():
    db.generate_db(models.Base)
