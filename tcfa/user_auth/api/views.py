import os
import jwt
from urllib.parse import quote_plus, urlencode
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .auth_utils import oauth
import dotenv

dotenv.load_dotenv()

from rest_framework import authentication, exceptions
import jwt


class Auth0TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, options={"verify_signature": False})
            user = self.get_or_create_user(payload)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

    def get_or_create_user(self, payload):
        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid payload")

        user, created = User.objects.get_or_create(username=user_id)
        return user

    def authenticate_header(self, request):
        return "Bearer"


def auth0_login(request):
    redirect_uri = request.build_absolute_uri("/user/auth/callback")
    return oauth.auth0.authorize_redirect(request, redirect_uri)


def auth0_callback(request):
    try:
        token = oauth.auth0.authorize_access_token(request)
        id_token = token.get("id_token", None)

        if id_token is None:
            raise ValueError("No id_token found in the request")

        if id_token:
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})

        return JsonResponse(
            {"message": "Authentication successful","token": token}
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def logout(request):
    request.session.clear()
    return_to = request.build_absolute_uri("/")
    return redirect(
        f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/v2/logout?client_id={settings.SOCIAL_AUTH_AUTH0_KEY}&returnTo={return_to}"
    )

def get_user(request):
    user = request.session.get("user", None)
    return JsonResponse({"user": user})