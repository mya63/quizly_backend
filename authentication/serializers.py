from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Adds password confirmation validation and creates a new user
    with Django's built-in create_user method.
    """

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "confirmed_password", "email"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        """
        Validates that password and confirmed_password match.

        Args:
            attrs (dict): Incoming serializer data.

        Returns:
            dict: Validated data.

        Raises:
            serializers.ValidationError: If passwords do not match.
        """
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(
                {"confirmed_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Creates a new user after removing the confirmation field.

        Args:
            validated_data (dict): Validated serializer data.

        Returns:
            User: Newly created user instance.
        """
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)