from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^home/', views.home, name="chome"),
    url(r'^mobile/', views.mobile),
    url(r'^redirectpage/', views.redirect_page),
    url(r'^hello', views.hello),
    url(r'^helloworld', views.helloworld),
    url(r'^students/$', views.students),
    url(r'^students/(\d+)/(\d+)/', views.students_id_age, name="students"),
    url(r'^getdate/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/', views.get_date, name="date"),
]