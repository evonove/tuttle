from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Provider(models.Model):
    name = models.CharField(null=True)


class User(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=255)


class Repository(models.Model):
    name = models.CharField(null=True)
    user = models.ForeignKey(User)


class DeployKey(models.Model):
    title = models.CharField(null=True, blank=False, max_length=50)
    key = models.CharField(null=True, blank=False, max_length=255)
    repository = models.ForeignKey(Repository)

