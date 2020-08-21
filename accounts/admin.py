from django.contrib import admin
from django.contrib.auth.models import Group

from . import forms, models


class UserAdmin(admin.ModelAdmin):
    form = forms.UpdateUserForm
    list_display = ('username', 'first_name', 'last_name', 'email')


admin.site.register(models.User, UserAdmin)
admin.site.unregister(Group)
