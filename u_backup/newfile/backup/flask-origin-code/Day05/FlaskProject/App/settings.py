def get_db_uri(dbinfo):

    database = dbinfo.get("DATABASE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(database, driver, user, password, host, port, name)


class Config:
    SECRET_KEY = "rock1204"

    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True

    dbinfo = {
        "DATABASE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskProject"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rock1204@localhost:3306/FlaskProject"


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rock1204@localhost:3306/FlaskProject"


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rock1204@localhost:3308/FlaskProject"


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": ProductConfig
}