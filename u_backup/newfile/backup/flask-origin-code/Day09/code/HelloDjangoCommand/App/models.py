from django.db import models


class Car(models.Model):

    c_logo = models.CharField(max_length=32)
    c_price = models.FloatField(default=1)
    c_type = models.CharField(max_length=16)


class Grade(models.Model):

    g_name = models.CharField(max_length=32,unique=True)


class Student(models.Model):

    s_name = models.CharField(max_length=32)
    s_age = models.IntegerField(default=18)
    s_grade = models.ForeignKey(Grade)