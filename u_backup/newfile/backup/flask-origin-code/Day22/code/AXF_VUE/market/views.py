from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from market.models import Goods, FoodType
from market.serializers import GoodsSerializer, FoodTypeSerializer

ALL_TYPES = "0"

ORDER_DEFAULT = "0"
ORDER_PRICE_UP = "1"
ORDER_PRICE_DOWN = "2"
ORDER_SALE_DOWN = "3"


class GoodsView(ListAPIView):

    serializer_class = GoodsSerializer
    queryset = Goods.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        # 筛选
        # 1
        categoryid = self.request.query_params.get("typeid", "104749")

        queryset = queryset.filter(categoryid=categoryid)

        # 2
        childcid = self.request.query_params.get("childcid", "0")

        if childcid != ALL_TYPES:
            queryset = queryset.filter(childcid=childcid)
        # 3 order_by
        """
            rule 
                0  default
                1  price up
                2  price down
                3  sale down
        """
        order_by = self.request.query_params.get("order_by", "0")

        if order_by == ORDER_PRICE_UP:
            queryset = queryset.order_by("price")
        elif order_by == ORDER_PRICE_DOWN:
            queryset = queryset.order_by("-price")
        elif order_by == ORDER_SALE_DOWN:
            queryset = queryset.order_by("-productnum")

        return queryset


class FoodTypesView(ListAPIView):

    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()