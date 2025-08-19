from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from .token_models import UserToken

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
            if isinstance(raw_token, bytes):
                token_string = raw_token.decode('utf-8')
            else:
                token_string = str(raw_token)

            validated_user = UserToken.is_token_valid(token_string)
            
            if validated_user and validated_user.id == user.id:
                return True
            else:
                print(f"Token not found or inactive for user {user.id}")
                return False
                
        except UnicodeDecodeError as e:
            print(f"Token decode error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error in token validation: {e}", exc_info=True)
            return False
