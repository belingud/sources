import base64
import json

from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):

    print(request)

    print(type(request))

    print(request.path)

    print(request.method)

    print(request.GET)

    print(request.POST)

    print(request.FILES)

    # print(request.environ)
    #
    # d = request.environ
    #
    # for key, value in d.items():
    #     print(key, value)
    print(request.is_ajax())

    print(request.GET.get("hobby"))

    print(request.GET.getlist("hobby"))

    # return HttpResponse("Index")
    response = HttpResponse()

    # response.content = "这样也行?"
    response.write("啦啦啦啦")

    return response


def html(request):
    return render(request, 'TwoIndex.html')


def js(request):

    # data = [
    #     {"name": "小明"},
    #     {"name": "小红"},
    #     {"name": "小蓝"},
    #     {"name": "膜拜"},
    # ]
    #
    # return JsonResponse(data, safe=False)

    data = {
        "msg": "ok"
    }

    content = json.dumps(data)

    return HttpResponse(content, content_type="application/json", status=500)
    # return Http404()
    # return HttpResponseNotAllowed(["HEAD", "OPTIONS"])


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":

        username = request.POST.get("username")

        response = redirect(reverse("two:mine"))

        # response.set_cookie("username", username)
        # base64编码
        # username = base64.standard_b64encode(username.encode("utf-8")).decode("utf-8")

        # 将utf-8编码
        username_utf8 = username.encode("utf-8")

        username_base64 = base64.standard_b64encode(username_utf8)

        username = username_base64.decode("utf-8")

        response.set_signed_cookie("username", username, salt="110")

        return response


def mine(request):

    # username = request.COOKIES.get("username")
    username = request.get_signed_cookie("username", salt="110")

    if not username:
        return redirect(reverse("two:login"))

    # username = base64.standard_b64decode(username.encode("utf-8")).decode("utf-8")

    username_encode = username.encode("utf-8")

    username_base64 = base64.standard_b64decode(username_encode)

    username = username_base64.decode("utf-8")

    return render(request, "mine.html",locals())


def logout(request):

    response = redirect(reverse("two:login"))

    response.delete_cookie("username")

    return response
