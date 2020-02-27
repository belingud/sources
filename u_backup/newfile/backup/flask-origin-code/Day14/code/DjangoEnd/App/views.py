# import datetime
# from time import sleep
import io
import random
from time import time

from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page


# 缓存时间配置，是需要结合具体场景使用的， 最重要的是在于数据更新频率
# @cache_page(60*5)
from App.models import Blog


def index(request):

    # sleep(10)

    return HttpResponse("Index")


def search(request):

    # 创造一个用户唯一标识
    #   选一个唯一标识    登录的用户可用，用户名，token， cookie   未登录的用户 可以使用ip
    # META 元信息  和 environ 是等效
    ip = request.META.get("REMOTE_ADDR")

    print(ip)
    #
    # value = cache.get(ip)
    #
    # if value:
    #     return HttpResponse("十秒之内只能搜索一次")
    #
    # # 进行搜索
    # cache.set(ip, "哈哈哈", timeout=10)

    # 1分钟之内10次

    record = cache.get(ip) or []

    # 清洗数据   将请求记录超过60秒的全部删除
    while record and time() - record[-1] > 60:
        record.pop()

    # 剩下的就是60秒之内的数据
    if len(record) > 10:
        return HttpResponse("一分钟之内最多请求十次")

    record.insert(0, time())

    cache.set(ip, record, timeout=60)

    return HttpResponse("Search")


def get_code(request):

    image_size = (100, 50)

    background = get_color()

    # 画布构建
    image = Image.new("RGB", image_size, background)

    # 画笔
    image_draw = ImageDraw.Draw(image, "RGB")

    for i in range(1000):
        image_draw.point(
            (random.randrange(100), random.randrange(50)), fill=get_color()
        )

    code = generate_code()

    for i in range(len(code)):
        # 绘制
        image_draw.text(
            (20 * i + random.randrange(25), random.randrange(15)),
            code[i],
            font=get_font(),
            fill=get_color(),
        )

    # 内存流
    buffer = io.BytesIO()
    #
    image.save(buffer, "png")

    request.session["code"] = code

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def get_color():
    red = random.randrange(256)
    green = random.randrange(256)
    blue = random.randrange(256)

    return red, green, blue


def get_font():
    font = ImageFont.truetype(
        font="/home/rock/Python1903/Day14/DjangoEnd/static/fonts/ADOBEARABIC-BOLD.OTF",
        size=random.randrange(30, 50),
    )
    return font


def generate_code():
    source_code = "1234567890qwertyuiopasdfghjklzxcvbnmZXCVBNMASFGHJKLQWRTYUIOP"
    dest = ""
    for i in range(4):
        dest += random.choice(source_code)

    return dest


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":

        code = request.session.get("code")

        verify_code = request.POST.get("verify_code")

        if code.lower() != verify_code.lower():

            return HttpResponse("验证失败")

        return HttpResponse("验证成功")


def edit_blog(request):
    if request.method == "GET":
        return render(request, "blog.html")
    elif request.method == "POST":
        content = request.POST.get("content")

        Blog.objects.create(b_title="富文本", b_content=content)

        return HttpResponse("发表成功")
