# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooster', '0005_sdtdienst'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SdtDienst',
            new_name='StdDienst',
        ),
    ]
