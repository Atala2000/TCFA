import os
import jwt
from urllib.parse import quote_plus, urlencode
import requests
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
            payload = self.decode_jwt(token)
            user = self.get_or_create_user(payload)
            request.session['user_id'] = user.id  # Store user ID in the session
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

    def decode_jwt(self, token):
        """
        Decode JWT token without verifying the signature.
        This should be replaced with a more secure verification method in production.
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Error decoding token")

    def get_or_create_user(self, payload):
        """
        Get or create a user based on the payload from the JWT token.
        """
        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid payload")

        user, _ = User.objects.get_or_create(username=user_id)
        return user

    def authenticate_header(self, request):
        return "Bearer"
    

def auth0_login(request):
    redirect_uri = request.build_absolute_uri("/user/auth/callback")
    return oauth.auth0.authorize_redirect(request, redirect_uri)


def auth0_callback(request):
    """
    Callback endpoint after authentication with Auth0.
    """
    try:
        token = oauth.auth0.authorize_access_token(request)
        id_token = token.get("id_token", None)

        if id_token:
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            user_id = decoded_token.get("sub")
            user = User.objects.get_or_create(username=user_id)[0]
            request.session['user_id'] = user.id 

        return JsonResponse(
            {"message": "Authentication successful","token": token}
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def logout(request):
    """
    Log out the user by clearing the session.
    """
    request.session.flush()  
    return_to = request.build_absolute_uri("/")
    return redirect(
        f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/v2/logout?client_id={settings.SOCIAL_AUTH_AUTH0_KEY}&returnTo={quote_plus(return_to)}"
    )
