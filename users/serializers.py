from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
import uuid


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('id', 'email','password','first_name','last_name')  # Customize fields as needed

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['username'] = uuid.uuid4()
        user = User.objects.create(**validated_data)
        if password:
            # Hash the password using set_password method
            user.set_password(password)
            user.save()
        return user
    
    def validate_email(self, value):
        """
        Check if the provided email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def to_representation(self, instance):
        """
        Serialize user data excluding the password field.
        """
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret