from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_client",
            "is_freelancer",
            "is_active",
        )


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email
        data["is_client"] = self.user.is_client
        data["is_freelancer"] = self.user.is_freelancer
        data["is_active"] = self.user.is_active

        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
            "is_client",
            "is_freelancer",
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_client=validated_data.get("is_client", False),
            is_freelancer=validated_data.get("is_freelancer", False),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
