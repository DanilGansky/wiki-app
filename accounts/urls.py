from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('my-profile/',
         views.UserView.as_view(), name='user-profile'),
    path('my-profile/update/',
         views.UpdateUserView.as_view(), name='update-profile'),
    path('my-profile/delete/',
         views.DeleteUserView.as_view(), name='delete-profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
]
