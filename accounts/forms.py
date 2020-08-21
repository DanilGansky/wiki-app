from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets = {
            'password': forms.PasswordInput()
        }


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        widgets = {
            'password': forms.PasswordInput()
        }


class BaseUpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseUpdateUserForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.instance._prev_photo = self.instance.profile_photo
            self.instance._prev_password = self.instance.password


class UpdateUserForm(BaseUpdateUserForm):
    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'profile_photo')


class ChangePasswordForm(BaseUpdateUserForm):
    repeat_password = forms.CharField(max_length=128,
                                      widget=forms.PasswordInput(
                                          attrs={'minlength': 8}))

    class Meta:
        model = User
        fields = ('password', )
        widgets = {
            'password': forms.PasswordInput(attrs={'minlength': 8}),
        }

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = _('New password')

    def clean(self, *args, **kwargs):
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if new_password != repeat_password:
            raise ValidationError(
                {'password': ValidationError(_('Password mismatch!'))},
                code='invalid')
