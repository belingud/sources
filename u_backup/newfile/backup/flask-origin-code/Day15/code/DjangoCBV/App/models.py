from django.db import models


class Book(models.Model):

    b_name = models.CharField(max_length=32, verbose_name="书名")

    b_price = models.FloatField(default=1000, verbose_name="价钱")

    b_sale = models.BooleanField(default=False, verbose_name="打折")

    def __str__(self):
        return self.b_name


class Grade(models.Model):

    g_name = models.CharField(max_length=16, verbose_name="班级名称")

    def __str__(self):
        return self.g_name


class Student(models.Model):
    s_name = models.CharField(max_length=32, verbose_name="学生姓名")

    s_grade = models.ForeignKey(Grade)

    def __str__(self):
        return self.s_name