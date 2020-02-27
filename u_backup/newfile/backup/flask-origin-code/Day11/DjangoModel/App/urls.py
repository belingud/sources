from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^addgoods/', views.add_goods),
    url(r'^getgoods/', views.get_goods),
    url(r'^deletegoods/', views.delete_goods),
]