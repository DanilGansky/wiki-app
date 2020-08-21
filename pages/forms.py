from django import forms

from categories.models import Category

from .models import Page


class BasePageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasePageForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.instance._prev_background = self.instance.background_image
            self.instance._prev_title = self.instance.title


class PageForm(BasePageForm):
    class Meta:
        model = Page
        exclude = ('author', )

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['category'].queryset = Category.objects.filter(
                author=self.instance.author)


class PageAdminForm(BasePageForm):
    class Meta:
        model = Page
        fields = '__all__'
