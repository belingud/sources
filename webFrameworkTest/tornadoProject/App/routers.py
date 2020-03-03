from App.views import IndexHandler, DateHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/date/(?P<year>=\d+)/(?P<month>\d+)/(?P<day>\d+)/', DateHandler),
]
