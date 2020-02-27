from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):

    return HttpResponse("Index")


def login(request):

    a = None

    a.encode("utf-8")

    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")

        request.session['username'] = username

        return redirect(reverse("app:mine"))


def mine(request):

    username = request.session.get("username")

    if not username:
        return redirect(reverse("app:login"))

    return render(request, "mine.html", locals())


def logout(request):
    # cookie  session 一起干掉
    request.session.flush()

    return redirect(reverse("app:login"))
