# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-06 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0003_remove_marketingpreference_mailchimp_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingpreference',
            name='mailchimp_subscribed',
            field=models.NullBooleanField(),
        ),
    ]
