# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-22 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_usersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
