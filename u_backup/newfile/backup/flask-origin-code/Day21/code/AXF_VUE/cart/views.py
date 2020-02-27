from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class CartsView(GenericAPIView):

    def get(self, request):

        data = {
            "msg": "ok"
        }

        return Response(data)