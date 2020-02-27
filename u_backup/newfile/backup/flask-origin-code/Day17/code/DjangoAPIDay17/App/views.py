import uuid

from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, \
    CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from App.models import Animal, User
from App.serializers import AnimalSerializer, UserSerializer


class BookView(APIView):

    def get(self, request, pk):
        raise Http404()


#
# class AnimalsAPIView(ListCreateAPIView):
#
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer
#
#
# class AnimalAPIView(RetrieveUpdateDestroyAPIView):
#
#     serializer_class = AnimalSerializer
#     queryset = Animal.objects.all()


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def haha(self, request, *args, **kwargs):
        return Response({"msg": "haha"})


class UsersAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "register":
            return self.do_register(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        else:
            raise APIException(detail="please supply correct action [register, login]")

    def do_register(self, request, *args, **kwargs):

        print(type(request))
        print(type(self))

        return self.create(request, *args, **kwargs)

    def do_login(self, request, *args, **kwargs):
        u_name = request.data.get("u_name")
        u_password = request.data.get("u_password")

        user = User.get_user(u_name)

        if not user:
            raise APIException(detail="用户不存在")

        if not user.check_password(u_password):
            raise APIException(detail="密码错误")

        token = uuid.uuid4().hex

        # 存token

        data = {
            "msg": "ok",
            "status": HTTP_200_OK,
            "token": token
        }

        return Response(data)
