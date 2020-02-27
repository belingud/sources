from django.db import models


class Animal(models.Model):

    name = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Cat(Animal):

    c_color = models.CharField(max_length=32)


class Dog(Animal):

    d_leg = models.IntegerField(default=4)
