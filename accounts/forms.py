from django import forms

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


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'profile_photo')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.instance._prev_photo = self.instance.profile_photo
            self.instance._prev_password = self.instance.password
