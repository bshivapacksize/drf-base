import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from commons.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserRegisterSerializer(DynamicFieldsModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"read_only": True},
        }

    @staticmethod
    def validate_password(value):
        """
        Validates password complexity using regex.
        """
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and include at least one uppercase letter, "
                "one lowercase letter, one number, and one special character."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": ["Password and Confirm Password do not match."]}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
