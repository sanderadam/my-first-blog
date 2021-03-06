# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rooster', '0003_auto_20170122_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AddField(
            model_name='dienst',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dienst',
            name='begintijd',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='dienst',
            name='eindtijd',
            field=models.TimeField(),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
