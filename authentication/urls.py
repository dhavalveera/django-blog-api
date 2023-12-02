from django.urls import path

from .views import register, login, logout_view

urlpatterns = [
    path('register/', register, name='user-registration'),
    path('login/', login, name='user-login'),
    path('logout/', logout_view, name='user-logout')
]