from django.contrib import admin

from . import forms, models


class CategoryAdmin(admin.ModelAdmin):
    form = forms.CategoryAdminForm
    list_display = ('name', 'author', 'description')


admin.site.register(models.Category, CategoryAdmin)
