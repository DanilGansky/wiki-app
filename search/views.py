from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import search


@login_required(login_url=settings.LOGIN_URL)
def search_view(request):
    query_text = request.GET.get('q')
    context = search(query_text, request.user)
    return render(request, 'search_results.html', context)


@login_required(login_url=settings.LOGIN_URL)
def tag_search_view(request, tag):
    context = search(tag, request.user, tag_search=True)
    return render(request, 'search_results.html', context)
