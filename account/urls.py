from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('update/', views.user_update_profile, name='user_update_profile'),
    path('accounts/register/', views.user_registration, name='user_registration'),
    path('profile/<str:username>/', views.user_view_profile, name='user_view_profile'),
]
