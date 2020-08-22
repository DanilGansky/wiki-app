from django.template import Library

register = Library()


@register.filter
def prettify_date(date):
    return date.strftime('%b %d %Y')


@register.filter
def prettify_shared_status(shared_value):
    return 'Public' if shared_value else 'Private'
