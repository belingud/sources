from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^users/$', views.UsersAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/', views.UserAPIView.as_view()),
    url(r'^animals/$', views.AnimalsAPIView.as_view()),
    url(r'^animals/(?P<pk>\d+)/', views.AnimalAPIView.as_view()),
    url(r'^search/', views.SearchAPIView.as_view()),
]

