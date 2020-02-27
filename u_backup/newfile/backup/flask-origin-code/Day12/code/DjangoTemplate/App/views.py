from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):

    num = 10

    hobbies = ["study", "gaming", "coding", "reading", "riding", "sleeping"]

    value1 = "110"

    value2 = 110

    msg = "<h1>啦啦啦</h1>"

    return render(request, 'Index.html', locals())


def home(request):
    return render(request, 'home1.html', locals())


def mobile(request):

    data = {
        "msg": "ok",
        "status": 200
    }

    return JsonResponse(data)


def redirect_page(request):

    # a = 1/0
    #
    # # return redirect("/app/home/")
    # return HttpResponseRedirect("/app/home/")
    # return redirect(reverse("uapp:chome"))
    # return redirect(reverse("uapp:students", args=(100, 500)))
    # return redirect(reverse("uapp:date", args=(100, 500, 200)))
    return redirect(reverse("uapp:date", kwargs={
        "year": 2019,
        "month": 5,
        "day": 29
    }))


def hello(request):
    return HttpResponse("Hello")


def helloworld(request):
    return HttpResponse("HelloWorld")


def students(request):
    return HttpResponse("students")


def students_id(request, id):

    print(id)

    pa =  r'/home/rock/.virtualenvs'
    pa_win =  r'\\home\\rock\\\.virtualenvs'

    return HttpResponse("students id")


def students_id_age(request, id, age):

    print(id, age)

    return HttpResponse("id and age")


def get_date(request, month, year, day):

    print(year, month, day)

    return HttpResponse("xxx")