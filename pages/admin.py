from django.contrib import admin

from . import forms, models


class PageAdmin(admin.ModelAdmin):
    form = forms.PageAdminForm
    list_display = ('title', 'category',
                    'description', 'author', 'is_shared', 'tags')


admin.site.register(models.Page, PageAdmin)
