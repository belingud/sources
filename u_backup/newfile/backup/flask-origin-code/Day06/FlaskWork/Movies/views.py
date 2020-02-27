from flask import Blueprint, session, render_template, request, jsonify

from Users.models import User
from .models import Banner, Movie, Collect

movies_blue = Blueprint("movies_blue", __name__, url_prefix="/movies")


@movies_blue.route("/home/")
def home():

    username = session.get("username")
    icon = session.get("icon")

    print(username, icon)

    banners = Banner.query.all()

    movies = Movie.query.all()

    user_id = User.query.filter(User.name.__eq__(username)).first().id

    collects = Movie.query.filter(Collect.query.filter(Collect.user_id.__eq__(user_id))).all()
    return render_template("home_logined.html", username=username, icon=icon, banners=banners, collections=movies, collected=collects)


@movies_blue.route("/collect/", methods=["POST"])
def collect():

    movie_id = request.form.get("movie_id")

    print(movie_id)

    username = session.get("username")

    if not username:

        data = {
            "msg": "not login",
            "status": 900
        }

        return jsonify(data)

    user_id = User.query.filter(User.name.__eq__(username)).first().id

    print(user_id)

    collects = Collect.query.filter(Collect.user_id.__eq__(user_id)).filter(Collect.movie_id.__eq__(movie_id)).all()

    if collects:

        data = {
            "msg": "collected",
            "status": 901
        }

        return jsonify(data)

    collect = Collect(movie_id=movie_id, user_id=user_id)

    if collect.save():

        data = {
            "msg": "collect success",
            "status": 902
        }

        return jsonify(data)
    else:
        data = {
            "msg": "collect fail",
            "status": 903
        }

        return jsonify(data)


# @movies_blue.route("/collected/")
# def collected():
#     username = request.form.get("username")
#
#     user_id = User.query.filter(User.name.__eq__(username)).first().id
#
#     collects = Collect.query.filter(User.id.__eq__(user_id)).all()
#     movie_id = []
#     for movie in collects:
#         movie_id.append(movie.movie_id)
#     return
