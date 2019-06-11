# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-21 09:35
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_productfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productfile',
            name='user_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/utkarsh/f/ProjectEcommerce/src/static_cdn/protected_media'), upload_to=products.models.upload_product_file_loc),
        ),
    ]