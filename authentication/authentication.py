from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token
    from an HTTP-only cookie instead of the Authorization header.
    """

    def authenticate(self, request):
        """
        Authenticates the user using the access token cookie.

        Args:
            request: Incoming HTTP request.

        Returns:
            tuple | None: Authenticated user and validated token,
            or None if no token is present.
        """
        raw_token = request.COOKIES.get(settings.AUTH_COOKIE_ACCESS)

        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token