# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-06-02 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='b_price',
            field=models.FloatField(default=1000),
        ),
    ]