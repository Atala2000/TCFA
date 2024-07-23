from django.urls import path
from .views import auth0_login, auth0_callback, logout, get_user

urlpatterns = [
    path('auth/login/', auth0_login, name='auth0_login'),
    path('auth/callback/', auth0_callback, name='auth0_callback'),
    path('auth/logout/', logout, name='logout'),
    path('auth/user/', get_user, name='get_user'),
]

