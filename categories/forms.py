from django import forms

from .models import Category


class BaseCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseCategoryForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.instance._prev_icon = self.instance.icon
            self.instance._prev_name = self.instance.name


class CategoryForm(BaseCategoryForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'icon')


class CategoryAdminForm(BaseCategoryForm):
    class Meta:
        model = Category
        fields = '__all__'
