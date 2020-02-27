from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from App.models import User


class UserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            token = request.query_params.get("token")
            print(token)
            user_id = cache.get(token)

            user = User.objects.get(pk=user_id)
            # print(user)
            return user, token
        except Exception as e:
            print('aaa')


class SearchAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            token = request.data.get("token")
            print(token)
            user_id = cache.get(token)

            user = User.objects.get(pk=user_id)
            return user, token
        except Exception as e:
            print('bbb')
