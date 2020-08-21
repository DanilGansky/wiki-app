from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.db.models.functions import Greatest

from categories.services import get_categories_with_recent_pages
from pages.models import Page


def _get_private_or_shared_pages(user):
    return Page.objects.filter(Q(author=user) | Q(is_shared=True))


def _search_by_text(query_text, user):
    return _get_private_or_shared_pages(user) \
        .annotate(similarity=Greatest(
            TrigramSimilarity('title', query_text),
            TrigramSimilarity('description', query_text),
            TrigramSimilarity('category__name', query_text),
            TrigramSimilarity('content_markup_html', query_text),
            TrigramSimilarity('author__username', query_text),
        )).filter(similarity__gt=0.03).order_by('-similarity')


def _search_by_tag(tag, user):
    return _get_private_or_shared_pages(user) \
        .filter(tags__contains=[tag]).order_by('-date_update')


def _generate_context(**kwargs):
    context = {k: v for k, v in kwargs.items()}
    context['categories'] = get_categories_with_recent_pages(
        author=context['user'])
    return context


def search(query_text, user, tag_search=False):
    if tag_search:
        results = _search_by_tag(query_text, user)
    else:
        results = _search_by_text(query_text, user)
    return _generate_context(query_text=query_text,
                             user=user,
                             results=results,
                             tag_search=tag_search)
