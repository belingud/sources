from Users.routers import urlpatterns as user_urlpatterns
from App.routers import urlpatterns as app_urlpatterns

urlpatterns = app_urlpatterns + user_urlpatterns
