import uuid
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction, IntegrityError
from utils.mail import send_confirmation_email
from .token_models import UserToken
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    EmailConfirmationSerializer,
    ResendConfirmationSerializer,
    LoginSerializer
)
from constants.models import UserStatusChoices
from constants.messages import AuthMessages, ValidationMessages
from constants.messages import HTTPErrorMessages

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_confirmation_email(user, request)

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


class EmailConfirmationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']

        try:
            user = User.objects.get(confirmation_token=token)

            with transaction.atomic():
                user.status = UserStatusChoices.ACTIVATED
                user.confirmed_at = timezone.now()
                user.confirmation_token = None
                user.save()

                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                UserToken.create_tokens_for_user(
                    user=user,
                    access_token=str(access_token),
                    refresh_token=str(refresh),
                )

            return Response({
                'message': AuthMessages.EMAIL_CONFIRMED_SUCCESS,
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'error': ValidationMessages.INVALID_TOKEN
            }, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(f"Database integrity error in email confirmation: {e}")
            return Response({
                'error': HTTPErrorMessages.INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected error in email confirmation: {e}", exc_info=True)
            return Response({
                'error': HTTPErrorMessages.INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        token = request.query_params.get('token')

        if not token:
            return Response({
                'error': ValidationMessages.TOKEN_NOT_PROVIDED
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['token'] = token

        return self.post(request)


class ResendConfirmationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)

            user.confirmation_token = str(uuid.uuid4())
            user.confirmation_sent_at = timezone.now()
            user.save()

            send_confirmation_email(user, request)

            return Response({
                'message': AuthMessages.EMAIL_CONFIRMATION_RESENT
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'email': ValidationMessages.EMAIL_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error in resend confirmation: {e}", exc_info=True)
            return Response({
                'error': HTTPErrorMessages.INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        try:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            UserToken.create_tokens_for_user(
                user=user,
                access_token=str(access_token),
                refresh_token=str(refresh),
            )

            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except IntegrityError as e:
            print(f"Database integrity error in login: {e}")
            return Response({
                'error': ValidationMessages.DATABASE_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected error in login: {e}", exc_info=True)
            return Response({
                'error': HTTPErrorMessages.INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]

                UserToken.objects.filter(
                    access_token=access_token,
                    is_active=True
                ).update(is_active=False)

            return Response({
                'message': AuthMessages.LOGOUT_SUCCESS
            }, status=status.HTTP_200_OK)

        except IntegrityError as e:
            print(f"Database integrity error in logout: {e}")
            return Response({
                'message': AuthMessages.LOGOUT_SUCCESS
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Unexpected error in logout: {e}", exc_info=True)
            return Response({
                'message': AuthMessages.LOGOUT_SUCCESS
            }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
