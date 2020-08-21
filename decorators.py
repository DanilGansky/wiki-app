from django.shortcuts import get_object_or_404

from categories import services


def extend_context(view):
    _get_context_data = view.get_context_data

    def get_context_data(self, *args, **kwargs):
        context = _get_context_data(self, *args, **kwargs)
        context['categories'] = services.get_categories_with_recent_pages(
            author=self.request.user)

        if hasattr(view, 'title'):
            context['title'] = self.title
        return context

    view.get_context_data = get_context_data
    return view


def custom_get_object_for_user(view):
    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            self.model, username=self.request.user.username)

    view.get_object = get_object
    return view


def filter_queryset_by_current_user(view):
    _get_queryset = view.get_queryset

    def get_queryset(self, *args, **kwargs):
        queryset = _get_queryset(self, *args, **kwargs)
        return queryset.filter(author=self.request.user)

    view.get_queryset = get_queryset
    return view
