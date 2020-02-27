from django.conf.urls import url

from LearnRR import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^hello/', views.HelloView.as_view()),
]