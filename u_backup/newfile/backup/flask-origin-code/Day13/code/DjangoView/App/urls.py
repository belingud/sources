from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index, name="index"),
    url(r'^login/', views.login, name="login"),
    url(r'^mine/', views.mine, name="mine"),
    url(r'^logout/', views.logout, name="logout"),
]