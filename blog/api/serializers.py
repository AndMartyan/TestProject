from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post
from validate_email import validate_email


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'is_private']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if (len(password)) < 8 and password != (
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'):
            raise serializers.ValidationError({"password": "Пароль должен содержать 8 символов и букву верхнего или "
                                                           "нижнего регистров"})
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают,Пароль должен содержать 8 символов и "
                                                           "букву верхнего или нижнего регистров "})
        if not validate_email(email):
            raise serializers.ValidationError({"username": "Введите E-mail"})

        user = User(username=email)
        user.set_password(password)
        user.save()
        return user
