from django.http import HttpResponse
from django.shortcuts import render


def hehe(request):

    return HttpResponse("小伙子睡着了")