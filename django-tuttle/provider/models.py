from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Provider(models.Model):
    repository_name = models.TextField(max_length=100)
    deploy_key = models.TextField(blank=True)
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.repository_name
