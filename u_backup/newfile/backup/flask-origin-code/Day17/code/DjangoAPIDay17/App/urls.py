from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^books/(?P<pk>\d+)/', views.BookView.as_view()),
    # url(r'^animals/$', views.AnimalsAPIView.as_view()),
    # url(r'^animals/(?P<pk>\d+)/', views.AnimalAPIView.as_view()),
    url(r'^animals/$', views.AnimalViewSet.as_view(
        actions={
            "get": "haha",
            "post": "create"
        }
    )),
    # url(r'^animals/(?P<pk>\d+)/', views.AnimalAPIView.as_view()),
    url(r'^users/', views.UsersAPIView.as_view()),
]
