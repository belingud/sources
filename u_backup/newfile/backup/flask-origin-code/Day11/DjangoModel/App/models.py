from django.db import models
from django.db.models import Manager

from ModelRelation.models import User


class TeachManager(Manager):

    # 获取查询结果集
    def get_queryset(self):
        # 调用父类中的get_queryset方法    对数据过滤
        queryset = super().get_queryset().filter(is_delete=False)

        return queryset

    def create_goods(self, g_name, g_price=10):
        goods = self.model()
        goods.g_price = g_price
        goods.g_name = g_name

        goods.save()

        return goods


class Goods(models.Model):

    g_name = models.CharField(max_length=32)
    g_price = models.FloatField(default=1)
    # g_foo = models.ForeignKey(User, unique=True)

    is_delete = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    objects = TeachManager()
