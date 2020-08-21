from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('page/<slug:slug>/', views.PageView.as_view(), name='page-detail'),
    path('shared/<str:username>/<slug:slug>/',
         views.SharedPageView.as_view(), name='shared-page'),
    path('create/', views.CreatePageView.as_view(), name='create-page'),
    path('update/<slug:slug>/',
         views.UpdatePageView.as_view(), name='update-page'),
    path('delete/<slug:slug>/',
         views.DeletePageView.as_view(), name='delete-page'),
]
