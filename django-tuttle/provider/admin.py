from django.contrib import admin
from .models import Provider, User, DeployKey, Repository

# Register your models here.

admin.site.register(Provider)
admin.site.register(User)
admin.site.register(DeployKey)
admin.site.register(Repository)