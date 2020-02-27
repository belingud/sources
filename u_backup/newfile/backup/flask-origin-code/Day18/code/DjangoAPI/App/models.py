from django.db import models
from rest_framework.exceptions import APIException


class User(models.Model):

    u_name = models.CharField(max_length=16, unique=True)
    u_password = models.CharField(max_length=256)
    is_super = models.BooleanField(default=False)

    @classmethod
    def get_user(cls, u_name, u_password):
        try:
            user = User.objects.get(u_name=u_name)

            if not user.check_password(u_password):
                raise APIException(detail="密码错误")
            return user
        except Exception as e:
            print(e)
            raise APIException(detail="用户不存在")

    def check_password(self, u_password):

        return self.u_password == u_password


class Animal(models.Model):

    a_name = models.CharField(max_length=16)
    # related_name 指定关联字段名字    默认 模型_set   指定之后就是我们的 related_name的值
    a_user = models.ForeignKey(User, related_name="u_animals")
