# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-28 02:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='goods',
            managers=[
                ('goods_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
