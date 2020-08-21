from pages.models import Page

from .models import Category


def _get_overflow_size(pages, limit):
    return {'overflow': len(pages) > limit,
            'overflow_size': len(pages) - limit}


def get_pages_by_category_name(category_name, author):
    return Page.objects.filter(category__name=category_name,
                               author=author).order_by('-date_update')


def get_categories_with_recent_pages(author, count=5):
    data = []

    for category in Category.objects.filter(author=author):
        pages = get_pages_by_category_name(category_name=category.name,
                                           author=author)
        overflow_size = _get_overflow_size(pages, count)
        category_data = {'recent_pages': pages[:count],
                         'category_data': category}
        data.append({**category_data, **overflow_size})
    return data
