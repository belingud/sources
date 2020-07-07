from gevent import monkey

monkey.patch_all()

import gevent
from flask import Flask, current_app
import threading
import pymysql
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from sqlalchemy.dialects.mysql import INTEGER
from loguru import logger
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:vic~hell@47.102.98.115:3306/flask_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG"] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(INTEGER(unsigned=True), primary_key=True)  # 编号
    name = db.Column(db.String(20), nullable=False)
    pwd = db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<User %r>" % self.name


import random
from time import sleep
import multiprocessing.pool


def repatching(item):
    try:
        # 需要重新写回的module
        module = __import__(item)
        # 需要重写的属性
        saved = gevent.monkey.saved
        mapper = saved.get(item, {})
        for attr in mapper:
            old_value = mapper.get(attr)
            if not old_value:
                continue
            setattr(module, attr, old_value)
    except Exception as ex:
        logger.exception("[gevent] repatching fail error=%s" % ex)


def delay_print(t):
    sleep(t)
    print(t)


def main():
    repatching("threading")
    pool = multiprocessing.pool.Pool()
    rng = random.Random()
    rng.seed(random.SystemRandom().random())
    for i in range(2):
        pool.apply_async(delay_print, (rng.randrange(3, 5),))
    pool.close()
    pool.join()
    pool.terminate()


@app.route("/", methods=["POST"])
def index():
    saved = gevent.monkey.saved
    logger.info(f"keys: {list(saved.keys())}")
    logger.info(f'saved {saved["threading"]}')
    logger.info(f"equal app: {current_app is app}")
    return {"msg": "ok"}


@app.route("/test")
def test():
    import threading
    import time

    class ExampleThread(threading.Thread):
        def run(self):
            time.sleep(3)  # takes a few minutes to finish
            print("finished working")

    worker = ExampleThread()
    worker.start()
    print("this should be printed before the worker finished")
    return {"msg": "ok"}


@app.route("/process")
def process():
    main()
    return {"msg": "ok"}


@app.route("/count")
def count():
    return {"count": len(threading.enumerate())}


# @app.errorhandler(Exception)
def handler(error):
    return "error"


if __name__ == "__main__":
    # db.create_all()
    manager.run()
