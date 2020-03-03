from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from TornadoProject.settings import DATABASE


def get_db_uri(db_info):
    engine = db_info.get('ENGINE')
    driver = db_info.get('DRIVER')
    user = db_info.get('USER')
    password = db_info.get('PASSWORD')
    host = db_info.get('HOST')
    port = db_info.get('PORT')
    db = db_info.get('NAME')
    return "{}+{}://{}:{}@{}/{}".format(engine, driver, user, password, host, port, db)


# create database engine
engine = create_engine(get_db_uri(DATABASE))
# create base model and bind engine with Base
Base = declarative_base(bind=engine)

# can be called
DbSession = sessionmaker(bind=engine)

session = DbSession()
