# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0003_auto_20160829_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploykey',
            name='key',
            field=models.CharField(max_length=500),
        ),
    ]
