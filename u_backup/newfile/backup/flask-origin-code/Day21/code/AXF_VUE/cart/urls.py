from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'', views.CartsView.as_view()),
]