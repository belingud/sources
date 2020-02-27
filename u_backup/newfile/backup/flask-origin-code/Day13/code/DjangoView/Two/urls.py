from django.conf.urls import url

from Two import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^upload/', views.upload, name="upload"),
    url(r'^persons/', views.get_persons, name="persons"),
    url(r'^bbb/', views.bbb)
]