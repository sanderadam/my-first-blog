# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooster', '0014_dienst_feestdagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='chauffeur',
            name='email',
            field=models.EmailField(default='test@test.com', max_length=254),
            preserve_default=False,
        ),
    ]
