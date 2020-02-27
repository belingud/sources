import random
from time import sleep

from flask import Blueprint, request, abort

from FlaskProjectAdvanced.extension import cache
from .models import Movie

movie_blue = Blueprint("movie_blue", __name__, url_prefix="/movies")


@movie_blue.route("/")
def index():

    print("摇奖中")

    abort(500)

    if random.randrange(100) > 90:
        return "恭喜您中奖了"

    return "呵呵哒，嘻嘻睡吧"


@movie_blue.route("/learn/")
@cache.cached(timeout=60)
def learn():

    print("开始学习")
    sleep(10)
    print("终于学完了")

    return "睡着了，做梦了"

