import os
from time import sleep

from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from DjangoView.settings import MEDIA_ROOT
from Two.models import User, Person


def index(request):
    return HttpResponse("Index")


def upload(request):
    if request.method == "GET":
        return render(request, "upload.html")
    elif request.method == "POST":
        username = request.POST.get("username")

        icon = request.FILES.get("icon")

        # print(username, icon)
        # /2019-28-05/30/19/new_logo.png
        # save_filename = os.path.join(MEDIA_ROOT, icon.name)

        # with open(save_filename, "wb") as save_file:
        #     # chunks 将文件拆分成一块一块的 可迭代对象
        #     for part in icon.chunks():
        #         save_file.write(part)
        #         save_file.flush()

        user = User()
        user.username = username
        user.icon = icon
        user.save()

        return HttpResponse("Upload File")


# @cache_page(5*60)
def get_persons(request):
    # 从缓存中取
    result = cache.get("get_persons")

    if result:
        return result

    sleep(10)

    page = int(request.GET.get("page", 1))

    per_page = int(request.GET.get("per_page", 10))

    persons = Person.objects.all()
    # 构建分页器
    paginator = Paginator(persons, per_page)
    # 获取具体的某一页
    page_object = paginator.page(page)
    # 生成响应
    response = render(request, "PersonList.html", locals())
    # 存入缓存
    cache.set("get_persons", response, timeout=60*5)

    return response


def bbb(request):
    return render(request, "bbb.html")
