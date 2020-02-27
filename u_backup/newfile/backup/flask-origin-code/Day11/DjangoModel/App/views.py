import random

from django.http import HttpResponse
from django.shortcuts import render

from App.models import Goods


def index(request):

    print(type(Goods.objects))
    # print(type(Goods.goods_manager))

    return HttpResponse("看看")


def add_goods(request):

    # goods = Goods.objects.create(g_name="电脑%d"%random.randrange(100), g_price=random.randrange(100000))
    goods = Goods.objects.create_goods(g_name="电脑%d"%random.randrange(100))

    return HttpResponse("添加商品%d"%goods.id)


def get_goods(request):

    goods_list = Goods.objects.all()

    return render(request, "GoodsList.html", locals())


def delete_goods(request):

    Goods.objects.last().delete()

    return HttpResponse("删除成功")