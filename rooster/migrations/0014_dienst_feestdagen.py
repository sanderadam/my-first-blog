# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooster', '0013_auto_20170216_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='dienst',
            name='feestdagen',
            field=models.FloatField(default=1),
        ),
    ]
