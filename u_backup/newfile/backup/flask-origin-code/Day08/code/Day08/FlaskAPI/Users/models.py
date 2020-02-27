import hashlib
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from FlaskWork.ext import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    _password = db.Column(db.String(256))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        # self._password = hashlib.new("md5", password.encode("utf-8")).hexdigest()
        # self._password = generate_password_hash(password)
        cur = datetime.datetime.now()
        precode = hashlib.new(password.encode("utf-8"))
        lable = str(cur.hour).hexdigest() + precode
        self._password = lable

    def check_password(self, password):
        # return self._password == hashlib.new("md5", password.encode("utf-8")).hexdigest()
        # return check_password_hash(self._password, password)
        pass

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True
