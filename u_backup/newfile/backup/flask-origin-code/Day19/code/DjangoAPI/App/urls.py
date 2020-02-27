from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^cars/', views.CarsAPIView.as_view()),
]