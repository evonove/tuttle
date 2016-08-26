from django.conf import settings
from django.db import models


class Provider(models.Model):
    """
    Provider model: stores provider's name
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Repository(models.Model):
    """
    Repository model: stores the name of the repository and the user who own the repo
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class DeployKey(models.Model):
    """
    DeployKey model stores the deploy key parameters of a repository
    """
    title = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    repository = models.ForeignKey(Repository)

    def __str__(self):
        return self.title
