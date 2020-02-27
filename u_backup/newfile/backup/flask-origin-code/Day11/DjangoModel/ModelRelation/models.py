from django.db import models


class User(models.Model):

    u_name = models.CharField(max_length=32, unique=True)


class Vip(models.Model):

    v_level = models.IntegerField(default=0)

    v_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class Address(models.Model):

    a_addr = models.CharField(max_length=128)
    a_user = models.ForeignKey(User)


class Goods(models.Model):

    g_name = models.CharField(max_length=32)

    g_users = models.ManyToManyField(User)


class Animal(models.Model):

    name = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Cat(Animal):

    c_color = models.CharField(max_length=32)


class Dog(Animal):

    d_leg = models.IntegerField(default=4)
