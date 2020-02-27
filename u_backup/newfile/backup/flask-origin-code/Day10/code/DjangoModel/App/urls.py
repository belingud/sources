from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^getgames/', views.get_games),
    url(r'^addgame/', views.add_game),
    url(r'^getgame/', views.get_game),
    url(r'^addbooks/', views.add_books),
    url(r'^getbooks/', views.get_books),
    url(r'^getpraise/', views.get_praise),
    url(r'^getgrades/', views.get_grades),
    url(r'^getage/', views.get_age),
]