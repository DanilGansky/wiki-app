from django.urls import path

from . import views

app_name = 'knowledge_base'

urlpatterns = [
    path('', views.HubView.as_view(), name='hub'),
]
