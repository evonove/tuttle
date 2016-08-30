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
    Repository model: stores the name of the repository, the owner of the repo
    """
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    is_private = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    provider = models.ForeignKey(Provider)

    def __str__(self):
        return self.name


class DeployKey(models.Model):
    """
    DeployKey model stores the deploy key parameters of a repository
    """
    title = models.CharField(max_length=255)
    key = models.CharField(max_length=800)
    repository = models.ForeignKey(Repository)

    def __str__(self):
        return self.title
