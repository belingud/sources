from sqlalchemy import Integer, Column, String

from TornadoProject.ext import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_name = Column(String(32), unique=True)


