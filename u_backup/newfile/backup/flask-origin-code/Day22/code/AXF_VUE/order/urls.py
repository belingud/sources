from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'', views.OrdersView.as_view()),
]