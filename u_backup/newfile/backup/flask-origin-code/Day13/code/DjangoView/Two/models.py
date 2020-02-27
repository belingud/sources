from django.db import models


class User(models.Model):

    username = models.CharField(max_length=32)
    icon = models.ImageField(upload_to="%Y-%M-%D")


class Person(models.Model):
    p_name = models.CharField(max_length=32)