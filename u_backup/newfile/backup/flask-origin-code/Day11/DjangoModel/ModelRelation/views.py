import random

from django.http import HttpResponse
from django.shortcuts import render

from ModelRelation.models import User, Vip, Goods, Dog, Cat, Animal


def add_user(request):

    User.objects.create(u_name="站着的同学好帅%d" % random.randrange(10000))

    return HttpResponse("好帅")


def add_vip(request):

    user = User.objects.last()

    vip = Vip()
    vip.v_level = random.randrange(8)
    vip.v_user = user

    vip.save()

    return HttpResponse("添加Vip成功")


def delete_user(request):

    user = User.objects.last()

    user.delete()

    return HttpResponse("删除成功")


def delete_vip(request):

    vip = Vip.objects.last()

    vip.delete()

    return HttpResponse("vip删除成功")


def get_user(request):

    user = User.objects.last()
    vip = user.vip

    print(vip.id)

    return HttpResponse("获取成功")


def get_vip(request):

    vip = Vip.objects.last()

    user = vip.v_user

    print(user.id)
    return HttpResponse("Vip获取成功")


def get_addresses(request):

    user = User.objects.last()

    print(user.address_set)
    print(type(user.address_set))

    addresses = user.address_set.all()

    return HttpResponse("获取成功")


def add_goods(request):

    Goods.objects.create(g_name="mysql%d" % random.randrange(1000))

    return HttpResponse("Goods添加成功")


def user_goods(request):

    user = User.objects.last()

    goods = Goods.objects.last()

    print(type(user.goods_set))
    print(user.goods_set)
    # user = User()
    user.goods_set.add(goods)

    return HttpResponse("添加成功")


def goods_user(request):
    user = User.objects.last()

    goods = Goods.objects.last()

    print(goods.g_users)
    print(type(goods.g_users))

    goods.g_users.add(user)

    return HttpResponse("添加成功，商品主动添加用户")


def del_goods_user(request):

    user = User.objects.last()

    goods = Goods.objects.last()

    goods.g_users.remove(user)

    return HttpResponse("删除成功")


def get_goods(request):

    user = User.objects.last()

    goods_list = user.goods_set.all()

    return render(request, "GoodsList.html", locals())


def get_users(request):

    goods = Goods.objects.last()

    users = goods.g_users.all()

    return render(request, "UserList.html", locals())


def add_dog(request):

    Dog.objects.create(name="哈士奇", d_leg=3)

    return HttpResponse("拆家神器")


def add_cat(request):

    Cat.objects.create(name="汤姆", c_color="red")

    return HttpResponse("小猫")


def add_animal(request):

    Animal.objects.create(name="动物")

    return HttpResponse("小动物")
