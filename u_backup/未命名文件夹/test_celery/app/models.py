from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.


class Test(models.Model):
    id = models.AutoField('id', primary_key=True)
    name = models.CharField(_('姓名'), max_length=20)
    password = models.CharField(_('密码'), max_length=20)
