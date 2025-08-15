from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class DatabaseTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)

        if not self.is_token_valid_in_database(user, raw_token):
            raise AuthenticationFailed()

        return (user, validated_token)

    def is_token_valid_in_database(self, user, raw_token):
        try:
            user.refresh_from_db()
            stored_token = user.auth_token
            if stored_token is None:
                return False

            if isinstance(raw_token, bytes):
                token_string = raw_token.decode('utf-8')
            else:
                token_string = str(raw_token)

            return stored_token == token_string
        except Exception as e:
            return False
