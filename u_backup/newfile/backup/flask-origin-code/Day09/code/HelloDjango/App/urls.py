from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^home/', views.home),
    url(r'^books/', views.get_book),
    url(r'^createbook/', views.create_book),
]