from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow
from home.serializers import MainWheelSerializer, MainNavSerializer, MainMustBuySerializer, MainShopSerializer, \
    MainShowSerializer


class HomeView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        mainwheels = MainWheel.objects.all()

        main_wheels_serializer = MainWheelSerializer(mainwheels, many=True)

        mainnavs = MainNav.objects.all()

        main_navs_serializer = MainNavSerializer(mainnavs, many=True)

        mainmustbuys = MainMustBuy.objects.all()

        main_must_buys_serializer = MainMustBuySerializer(mainmustbuys, many=True)

        mainshops = MainShop.objects.all()

        main_shops_serializer = MainShopSerializer(mainshops, many=True)

        mainshows = MainShow.objects.all()

        main_shows_serializer = MainShowSerializer(mainshows, many=True)

        data = {
            "status": HTTP_200_OK,
            "msg": "ok",
            "data": {
                "main_wheels": main_wheels_serializer.data,
                "main_navs": main_navs_serializer.data,
                "main_must_buys": main_must_buys_serializer.data,
                "main_shops": main_shops_serializer.data,
                "main_shows": main_shows_serializer.data
            }
        }

        return Response(data)
