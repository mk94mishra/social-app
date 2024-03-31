from rest_framework import serializers

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS
from .models import FriendRequest
from users.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.cache import cache


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status', 'timestamp')


    