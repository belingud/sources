from django.db import models
from django.db.models import Q
from rest_framework.exceptions import NotFound


class UserModel(models.Model):

    u_name = models.CharField(max_length=32, unique=True, null=False, blank=False)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True, null=False, blank=False)
    u_icon = models.CharField(max_length=256, null=True, blank=True, default="")
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    @classmethod
    def check_username(cls, u_name):
        """
            检测用户名在数据库中是否存在，如果存在则返回true， false反之
                对应属性  __doc__
        :param u_name:
        :return: bool
        """
        return UserModel.objects.filter(u_name=u_name).exists()

    @classmethod
    def get_user(cls, u_user):
        """

        :param u_user:  用户标识, 可能是用户名或者邮箱
        :return:
        """
        user = UserModel.objects.filter(Q(u_name=u_user) | Q(u_email=u_user)).first()
        if not user:
            raise NotFound(detail="用户不存在")
        return user

    def check_password(self, u_password):
        return self.u_password == u_password

    class Meta:
        db_table = "user_model"