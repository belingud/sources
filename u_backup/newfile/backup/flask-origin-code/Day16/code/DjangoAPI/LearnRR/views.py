from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(["GET", "POST", "PUT"])
def index(request):

    print(request)

    print(type(request))

    # print(request.POST)

    print(request.data)

    # return HttpResponse("Index%d" % status.HTTP_200_OK)
    # return JsonResponse({"msg": "ok"})

    # data = {
    #     "msg": "ok"
    # }

    data = "啦啦啦德玛西亚"

    return Response(data)


class HelloView(APIView):

    def get(self, request):
        print(request)
        print(type(request))

        return Response("Hello View")
