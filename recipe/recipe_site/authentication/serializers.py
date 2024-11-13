from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """User registration and creation serializer"""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    """Client side should not be able to send token with request."""
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User

        # List all fields that could be included inside request
        fields = ["email", "username", "password", "token"]

        def create(self, validated_data):
            # New user creation
            return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    # Method validate makes sure that current instance
    # LoginSerializer is valid
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in")

        if password is None:
            raise serializers.ValidationError("A password is required to log in")

        user = authenticate(username=email, password=password)
        # If user does not exists in db None will be returned, so raice exceprtion
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found"
            )
        # Make sure that flag is_active is false
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated")

        return {"email": user.email, "username": user.username, "token": user.token}
