import uuid

from django.core.cache import cache
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django_filters.rest_framework import DurationFilter, DjangoFilterBackend
from App.authentication import UserTokenAuthentication
from App.models import User, Animal
from App.permissions import LoginPermission, SearchPermission
from App.serializers import UserSerializer, AnimalSerializer
from App.throttle import VisitThrottle
from DjangoAPI.settings import ADMIN_USERS


class UsersAPIView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == "register":
            return self.create(request, *args, **kwargs)
        elif action == "login":
            return self.do_login(request, *args, **kwargs)
        else:
            raise APIException("请提供正确的动作")

    def perform_create(self, serializer):

        # if serializer.validated_data.get("u_name") in ADMIN_USERS:
        #     is_super = True
        # else:
        #     is_super = False
        #
        # serializer.save(is_super=is_super)
        serializer.save(is_super=serializer.validated_data.get("u_name") in ADMIN_USERS)

    def do_login(self, request, *args, **kwargs):

        u_name = request.data.get("u_name")
        u_password = request.data.get("u_password")

        user = User.get_user(u_name, u_password)

        token = uuid.uuid4().hex

        cache.set(token, user.id, timeout=60*60*24*7)

        data = {
            "msg": "login success",
            "status": HTTP_200_OK,
            "token": token
        }

        return Response(data)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = UserTokenAuthentication,
    permission_classes = LoginPermission,


class AnimalsAPIView(ListCreateAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    authentication_classes = UserTokenAuthentication,
    permission_classes = LoginPermission,

    def perform_create(self, serializer):
        serializer.save(a_user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_super:
            queryset = queryset.filter(a_user=self.request.user)

        return queryset


class AnimalAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    authentication_classes = UserTokenAuthentication,
    permission_classes = LoginPermission,


class SearchAPIView(RetrieveAPIView):
    authentication_classes = UserTokenAuthentication,
    permission_classes = SearchPermission,
    filter_backends = DjangoFilterBackend,
    fields = ('a_name', "u_name")
    throttle_classes = VisitThrottle,

    def get_queryset(self):
        print('get_u_name')
        queryset = User.objects.all()
        search_name = self.request.query_params.get("u_name")
        print("search_name:", search_name)
        print("query_set:", queryset)
        try:
            user = queryset.get(u_name=search_name)
            print("user:", user)
            queryset = queryset.all()
            return queryset
        except Exception as e:
            queryset = Animal.objects.all()
            print(e)
            queryset = queryset.all()

            print("final_queryset:", queryset)
            return queryset

        # search in user queryset, if not exist chang the queryset into animal queryset
        # try:
        #     query_set = Animal.objects.all()
        #     query_set.get(a_name=search_name)
        #     print(query_set)
        #     print('animal_queryset')
        #
        #     return query_set
        # except Exception as e:
        #     query_set = User.objects.all()
        #     print('user_queryset')
        #     return query_set.all()

    def get_serializer(self, *args, **kwargs):
        search_item = self.request.query_params.get("u_name")
        print("search_item", search_item)
        print('get_serializer_class')
        print(self.queryset)
        try:
            self.queryset.get(u_name=search_item)
            print('animal')
            serializer_class = AnimalSerializer
            return serializer_class(*args, **kwargs)
        except Exception as e:
            print(e)
            serializer_class = UserSerializer
            print('ddd')
            return serializer_class(*args, **kwargs)

    # def get_object(self):
    #     return self.request.user

    def get_object(self):
        print("get_object")
        return self.filter_queryset(self.get_queryset())
        # # Perform the lookup filtering.
        # lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        #
        # filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # obj = get_object_or_404(queryset, **filter_kwargs)
        # self.check_object_permissions(self.request, obj)
        #
        # return obj
