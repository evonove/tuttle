from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


class TuttleUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class CustomUserAdmin(UserAdmin):
    form = TuttleUserForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('token', )}),
    )

admin.site.register(get_user_model(), CustomUserAdmin)
