from django.db import models


class Animal(models.Model):

    a_name = models.CharField(max_length=16)
    a_leg = models.IntegerField(default=4)


class User(models.Model):

    u_name = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)

    @classmethod
    def get_user(cls, u_name):
        try:
            user = User.objects.get(u_name=u_name)
            return user
        except Exception as e:
            print(e)

    def check_password(self, password):
        return self.u_password == password