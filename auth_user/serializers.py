from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели кастомного пользователя"""
    username = serializers.CharField(
        required=True,
        allow_null=True,
        allow_blank=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )

    role = serializers.CharField(default='user', allow_null=True,
                                 allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role',
                  'bio', 'first_name', 'last_name')


class EmailSerializer(serializers.Serializer):
    """Сериалайзер для электронной почты пользователя"""
    email = serializers.EmailField(required=True)


class ConfirmationSerializer(serializers.Serializer):
    """Сериалайзер для письма с кодом подтверждения"""
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.SlugField(max_length=100, required=True)
