from django.urls import path

from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search-view'),
    path('tag/<str:tag>/', views.tag_search_view, name='tag-search'),
]
