from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TuttleUser(AbstractUser):
    email = models.EmailField(_('Email address'), max_length=254, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    token = models.CharField(null=True, blank=True, max_length=254, unique=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name