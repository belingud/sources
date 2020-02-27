from FlaskWork.ext import db
from common.models import BaseModel


class User(BaseModel):

    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    icon = db.Column(db.String(256), nullable=True)

    def check_password(self, password):
        return self.password == password
