from django.db import models


class Game(models.Model):

    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=32, unique=True, null=False, blank=False)
    # default 不会在数据中有所体现
    g_price = models.IntegerField(default=1)

    @classmethod
    def create(cls, g_name="QQGame", g_price=10):
        game = Game.objects.create(g_name=g_name, g_price=g_price)
        return game

    """
        这是元信息
    """
    class Meta:
        db_table = "gaming"
        # 排序是一个元组， 是根据元组中的元素顺序进行排序的， 最前面的优先级别最高，当前一位相等会根据后一位进行继续排序
        ordering = "g_price", "-g_id",


class Book(models.Model):

    b_name = models.CharField(max_length=32)

    b_publish_date = models.DateField(auto_now=True)


class Praise(models.Model):

    p_content = models.CharField(max_length=64)
    p_book = models.ForeignKey(Book)


class Grade(models.Model):

    g_name = models.CharField(max_length=32)

    g_boy_nums = models.IntegerField(default=10)

    g_girl_nums = models.IntegerField(default=70)


class Student(models.Model):

    s_name = models.CharField(max_length=32)

    s_age = models.IntegerField(default=18)

    s_grade = models.ForeignKey("Grade")