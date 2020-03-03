from Users.views import UserHandler, DBHandler

urlpatterns = [
    (r'/users/', UserHandler),
    (r'/db/', DBHandler),
]
