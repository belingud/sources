from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^search/', views.search),
    url(r'^getcode/', views.get_code, name="get_code"),
    url(r'^login/', views.login, name="login"),
    url(r'^editblog/', views.edit_blog, name="blog"),
]