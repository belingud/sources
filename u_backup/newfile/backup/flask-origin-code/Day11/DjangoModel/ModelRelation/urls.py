from django.conf.urls import url

from ModelRelation import views

urlpatterns = [
    url(r'^adduser/', views.add_user),
    url(r'^addvip/', views.add_vip),
    url(r'^deleteuser/', views.delete_user),
    url(r'^deletevip/', views.delete_vip),
    url(r'^getuser/', views.get_user),
    url(r'^getvip/', views.get_vip),

    url(r'^getaddresses/', views.get_addresses),

    url(r'^addgoods/', views.add_goods),
    url(r'^usergoods/', views.user_goods),

    url(r'^goodsuser/', views.goods_user),
    url(r'^delgoodsuser/', views.del_goods_user),

    url(r'^getgoods/', views.get_goods),
    url(r'^getusers/', views.get_users),

    url(r'^adddog/', views.add_dog),
    url(r'^addcat/', views.add_cat),
    url(r'^addanimal/',views.add_animal),

]