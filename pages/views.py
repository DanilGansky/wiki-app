from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from decorators import extend_context, filter_queryset_by_current_user

from .forms import PageForm
from .models import Page


class BasePageView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL
    model = Page
    context_object_name = 'page'


class BasePageEditView(BasePageView):
    template_name = 'form.html'
    form_class = PageForm


@extend_context
@filter_queryset_by_current_user
class PageView(BasePageView, DetailView):
    template_name = 'page_detail.html'


@extend_context
class SharedPageView(BasePageView, DetailView):
    template_name = 'page_detail.html'
    queryset = Page.shared

    def get_queryset(self):
        return super(SharedPageView, self).get_queryset() \
            .filter(author__username=self.kwargs.get('username'))


@extend_context
class CreatePageView(BasePageEditView, CreateView):
    title = _('Create page')

    def get_form_kwargs(self):
        kwargs = super(CreatePageView, self).get_form_kwargs()
        kwargs['instance'] = self.model(author=self.request.user)
        return kwargs


@extend_context
@filter_queryset_by_current_user
class UpdatePageView(BasePageEditView, UpdateView):
    title = _('Update page')


@extend_context
@filter_queryset_by_current_user
class DeletePageView(BasePageView, DeleteView):
    success_message = _('Page "{title}" successfully deleted')
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        category = self.object.category
        return reverse_lazy('categories:category-detail',
                            kwargs={'slug': category.slug})

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message.format(
            title=self.get_object().title))
        return super(DeletePageView, self).delete(request, *args, **kwargs)
