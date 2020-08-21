from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from decorators import extend_context, filter_queryset_by_current_user

from . import forms, services
from .models import Category


class BaseCategoryView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL
    model = Category
    context_object_name = 'category'


class BaseCategoryEditView(BaseCategoryView):
    template_name = 'form.html'
    form_class = forms.CategoryForm


@extend_context
@filter_queryset_by_current_user
class CategoryView(BaseCategoryView, DetailView):
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['pages'] = services.get_pages_by_category_name(
            category_name=self.object.name, author=self.request.user)
        return context


@extend_context
class CreateCategoryView(BaseCategoryEditView, CreateView):
    title = _('Create category')

    def get_form_kwargs(self):
        kwargs = super(CreateCategoryView, self).get_form_kwargs()
        kwargs['instance'] = Category(author=self.request.user)
        return kwargs


@extend_context
@filter_queryset_by_current_user
class UpdateCategoryView(BaseCategoryEditView, UpdateView):
    title = _('Update category')


@extend_context
@filter_queryset_by_current_user
class DeleteCategoryView(BaseCategoryView, DeleteView):
    success_message = _('Category "{name}" successfully deleted')
    success_url = '/'
    template_name = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message.format(
            name=self.get_object().name))
        return super(DeleteCategoryView, self).delete(request, *args, **kwargs)
