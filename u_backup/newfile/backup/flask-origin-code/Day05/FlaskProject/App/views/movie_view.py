from flask import Blueprint
from App.models import Movie


movie_blue = Blueprint("movie_blue", __name__, url_prefix="/movies")


@movie_blue.route("/")
def index():
    return "Movie Index"