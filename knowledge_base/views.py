from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from categories import services


class HubView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request):
        categories = services.get_categories_with_recent_pages(
            author=request.user)
        return render(request, 'index.html', {'categories': categories})
