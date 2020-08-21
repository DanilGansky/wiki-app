from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('category/<slug:slug>/',
         views.CategoryView.as_view(), name='category-detail'),
    path('create/',
         views.CreateCategoryView.as_view(), name='create-category'),
    path('update/<slug:slug>/',
         views.UpdateCategoryView.as_view(), name='update-category'),
    path('delete/<slug:slug>/',
         views.DeleteCategoryView.as_view(), name='delete-category'),
]
