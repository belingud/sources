from django.conf.urls import url

from Two import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^html/', views.html),

    url(r'^js/', views.js),
    url(r'^login/', views.login, name="login"),
    url(r'^mine/', views.mine, name="mine"),
    url(r'^logout/', views.logout, name="logout")
]