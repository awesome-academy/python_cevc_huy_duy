from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
import uuid
from django.utils import timezone
from constants.messages import ValidationMessages, AuthMessages
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            'min_length': ValidationMessages.MIN_LENGTH.format(length=8),
            'required': ValidationMessages.REQUIRED,
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'password_confirm'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                ValidationMessages.EMAIL_ALREADY_EXISTS
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                ValidationMessages.USERNAME_ALREADY_EXISTS
            )
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except Exception as exc:
            raise serializers.ValidationError(exc.messages)
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': ValidationMessages.PASSWORD_MISMATCH
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        confirmation_token = str(uuid.uuid4())

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            confirmation_token=confirmation_token,
            confirmation_sent_at=timezone.now()
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'status',
            'date_joined',
            'confirmed_at'
        ]
        read_only_fields = ['id', 'date_joined', 'status', 'confirmed_at']


class EmailConfirmationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        try:
            user = User.objects.get(confirmation_token=value)
            if user.confirmed_at:
                raise serializers.ValidationError(
                    AuthMessages.ACCOUNT_ALREADY_CONFIRMED
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(ValidationMessages.INVALID_TOKEN)

        return value


class ResendConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.confirmed_at:
                raise serializers.ValidationError(
                    AuthMessages.ACCOUNT_ALREADY_CONFIRMED
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                ValidationMessages.EMAIL_NOT_FOUND
              )

        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError({
                'password': AuthMessages.INVALID_CREDENTIALS
            })

        if not user.confirmed_at:
            raise serializers.ValidationError({
                'email': AuthMessages.ACCOUNT_NOT_CONFIRMED
            })

        attrs['user'] = user

        return attrs
