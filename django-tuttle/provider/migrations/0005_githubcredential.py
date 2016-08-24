# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0004_provider_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
    ]
