from django.urls import path
from . import views


urlpatterns = [
    path('', views.FriendListView.as_view(), name='friend_list'),  # List friends

    path('pending-requests/', views.PendingFriendRequestListView.as_view(), name='pending_friend_requests/'),  # List pending requests

    path('friend-requests/', views.FriendRequestViewCreate.as_view(), name='friend_request_create'),  # Create friend request

    path('friend-requests/<int:pk>/', views.FriendRequestViewUpdate.as_view(), name='friend_request_update'),  # update friend request
]
