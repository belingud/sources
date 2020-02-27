from django.conf.urls import url
from django.views.generic import TemplateView

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^hello/', views.HelloView.as_view(msg="HeHe")),
    # url(r'^customview/', views.HelloCustomView.as_view()),
    url(r'^customview/', views.HelloCustomView().dispatch),
    # url(r'^template/', views.HelloTemplateView.as_view()),
    # url(r'^template/', TemplateView.as_view(template_name="HelloTemplate.html")),
    url(r'^template/', views.HelloTemplateView.as_view(template_name="HelloTemplate.html")),
    url(r'^booklist/', views.HelloListView.as_view()),
    url(r'^details/', views.HelloDetailView.as_view(), name='bookdetail'),
]