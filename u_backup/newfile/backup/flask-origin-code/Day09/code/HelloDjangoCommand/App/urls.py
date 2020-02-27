from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^addgrade/', views.add_grade),
    url(r'^getgrades/', views.get_grades),

    url(r'^addstudent/',views.add_student),

    url(r'^getgrade/', views.get_grade),
]