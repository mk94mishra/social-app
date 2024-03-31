from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include user app URLs
    path('friends/', include('friends.urls')),  # Include friend app URLs
]
