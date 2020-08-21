from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from decorators import custom_get_object_for_user, extend_context

from .forms import LoginForm, SignUpForm, UpdateUserForm
from .models import User
from .services import InvalidCredentials, create_user, get_user


class BaseUserView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL
    model = User


class BaseAuthView(View):
    template = 'form.html'

    def get(self, request):
        logout(request)
        messages.warning(request, _('You are logged out'))
        return render(request, self.template, {'form': self.form(),
                                               'title': self.title})


@extend_context
@custom_get_object_for_user
class UserView(BaseUserView, DetailView):
    template_name = 'user_detail.html'


@extend_context
@custom_get_object_for_user
class UpdateUserView(BaseUserView, UpdateView):
    title = _('Edit profile')
    template_name = 'form.html'
    form_class = UpdateUserForm


@extend_context
@custom_get_object_for_user
class DeleteUserView(BaseUserView, DeleteView):
    success_url = '/'
    success_message = _('Profile "{username}" successfully deleted')
    template_name = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message.format(
            username=self.get_object().username))
        return super(DeleteUserView, self).delete(request, *args, **kwargs)


class LoginView(BaseAuthView):
    form = LoginForm
    title = _('Login')

    def post(self, request):
        try:
            user = get_user(request.POST.get('username'),
                            request.POST.get('password'))
        except InvalidCredentials:
            messages.error(request, _('Invalid username or password'))
            return render(request, self.template, {'form': self.form,
                                                   'title': self.title})
        else:
            login(request, user)
            messages.success(request, _(f'Hello, {user.username}'))
            return redirect(request.GET.get('next', '/'))


class SignUpView(BaseAuthView):
    form = SignUpForm
    title = _('Sign Up')

    def post(self, request):
        form = self.form(request.POST)

        try:
            create_user(form)
        except InvalidCredentials:
            messages.error(request, _('Invalid credentials'))
            return render(request, self.template, {'form': form,
                                                   'title': self.title})
        else:
            return redirect(reverse('accounts:login'))
