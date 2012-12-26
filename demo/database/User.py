from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, BigInteger, String

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from Base import Base
from SessionFactory import SessionFactory

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    permission_level = Column(Integer)

    def __init__(self, username, permission_level=0):
        self.username = username
        self.permission_level = permission_level

    def __repr__(self):
        return "<User('%s', '%d')>" % (self.username, self.permission_level)
