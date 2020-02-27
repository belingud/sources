from rest_framework import routers

from App import views

router = routers.DefaultRouter()

router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"books", views.BookViewSet)
