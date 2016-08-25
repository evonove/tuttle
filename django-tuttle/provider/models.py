from django.conf import settings
from django.db import models


class Provider(models.Model):
    name = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.name


class Repository(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class DeployKey(models.Model):
    title = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    repository = models.ForeignKey(Repository)

    def __str__(self):
        return self.title
