# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooster', '0012_dienst_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dienst',
            name='comments',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
