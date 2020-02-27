from django.conf.urls import url

from Blogs import views

urlpatterns = [
    url(r'^hehe/', views.hehe),
]