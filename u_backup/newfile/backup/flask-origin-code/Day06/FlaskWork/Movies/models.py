from FlaskWork.ext import db
from Users.models import User
from common.models import BaseModel


class Banner(BaseModel):

    image = db.Column(db.String(256))


class Movie(BaseModel):

    postid = db.Column(db.Integer)

    title = db.Column(db.String(128))

    image = db.Column(db.String(256))

    duration = db.Column(db.Integer)


class Collect(BaseModel):

    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
