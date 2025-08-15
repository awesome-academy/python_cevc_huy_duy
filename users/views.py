import uuid
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from utils.mail import send_confirmation_email
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    EmailConfirmationSerializer,
    ResendConfirmationSerializer
)
from constants.models import UserStatusChoices
from constants.messages import AuthMessages, ValidationMessages

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

            user.status = UserStatusChoices.ACTIVATED
            user.confirmed_at = timezone.now()
            user.confirmation_token = None
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

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
        user = User.objects.get(email=email)

        user.confirmation_token = str(uuid.uuid4())
        user.confirmation_sent_at = timezone.now()
        user.save()

        send_confirmation_email(user, request)

        return Response({
            'message': AuthMessages.EMAIL_CONFIRMATION_RESENT
        }, status=status.HTTP_200_OK)
