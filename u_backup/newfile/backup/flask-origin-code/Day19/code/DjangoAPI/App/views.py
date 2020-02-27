from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from App.models import Car
from App.serializers import CarSerializer
from App.throttling import LearnThrottle


class CarsAPIView(ListCreateAPIView):

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    # throttle_classes = LearnThrottle,


@api_view(["GET", "POST"])
@throttle_classes([LearnThrottle,])
def haha(request):

    data = {
        "msg": "haha"
    }

    return Response(data)