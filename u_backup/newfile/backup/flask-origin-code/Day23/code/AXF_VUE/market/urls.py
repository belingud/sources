from django.conf.urls import url

from market import views

urlpatterns = [
    url(r'^goods/', views.GoodsView.as_view()),
    url(r'^foodtypes/', views.FoodTypesView.as_view()),
]