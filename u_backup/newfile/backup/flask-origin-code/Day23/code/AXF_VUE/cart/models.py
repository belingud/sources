from django.db import models

from market.models import Goods
from user.models import UserModel


class CartModel(models.Model):

    c_user = models.ForeignKey(UserModel)
    c_goods = models.ForeignKey(Goods)
    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)