from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='user-list'),  # Map UserView to /users/ endpoint
    path('login/refresh-token', views.TokenRefreshView.as_view(), name='refresh-token'),  # Refresh token view
    path('login/', views.LoginView.as_view(), name='login'),  # Login view
    path('search/', views.SearchUserView.as_view(), name='search_users'),  # Search users
]
