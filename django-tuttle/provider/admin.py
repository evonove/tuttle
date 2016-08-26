from django.contrib import admin

from .models import Provider, DeployKey, Repository


admin.site.register(Provider)
admin.site.register(DeployKey)
admin.site.register(Repository)
