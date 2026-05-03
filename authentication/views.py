from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import RegisterSerializer


def set_auth_cookies(response, access_token, refresh_token=None):
    """
    Stores the access token and optional refresh token
    in HTTP-only cookies.

    Args:
        response (Response): DRF response object.
        access_token (str): JWT access token.
        refresh_token (str | None): JWT refresh token.
    """
    response.set_cookie(
        settings.AUTH_COOKIE_ACCESS,
        str(access_token),
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )

    if refresh_token is not None:
        response.set_cookie(
            settings.AUTH_COOKIE_REFRESH,
            str(refresh_token),
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )


def clear_auth_cookies(response):
    """
    Deletes authentication cookies from the response.

    Args:
        response (Response): DRF response object.
    """
    response.delete_cookie(settings.AUTH_COOKIE_ACCESS)
    response.delete_cookie(settings.AUTH_COOKIE_REFRESH)


class RegisterView(APIView):
    """
    Handles user registration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validates the registration data and creates a new user.

        Returns:
            Response: Success or validation error response.
        """
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {"detail": "User created successfully!"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Handles user login and sets JWT cookies.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticates the user with username and password.

        On success, access and refresh tokens are stored
        in HTTP-only cookies.

        Returns:
            Response: Login success or invalid credentials response.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(response, access, refresh)
        return response


class LogoutView(APIView):
    """
    Handles user logout and blacklists the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logs the authenticated user out, blacklists the refresh token,
        and removes authentication cookies.

        Returns:
            Response: Logout success or token error response.
        """
        refresh_token = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except AttributeError:
            pass
        except TokenError:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "detail": (
                    "Log-Out successfully! All Tokens will be deleted. "
                    "Refresh token is now invalid."
                )
            },
            status=status.HTTP_200_OK,
        )

        clear_auth_cookies(response)
        return response


class TokenRefreshCookieView(APIView):
    """
    Refreshes the access token using the refresh token from cookies.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new access token from the refresh token cookie.

        Returns:
            Response: Token refresh success or error response.
        """
        refresh_token = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
        except TokenError:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"detail": "Token refreshed"},
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(response, access_token)
        return response