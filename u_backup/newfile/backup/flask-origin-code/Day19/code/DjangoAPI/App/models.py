from django.db import models


class Car(models.Model):

    c_name = models.CharField(max_length=32)
