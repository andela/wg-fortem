from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import SocialLoginSerializer

from social_django.utils import load_strategy, load_backend

from requests.exceptions import HTTPError

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend, AuthForbidden


class SocialLoginView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = SocialLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None
            )

        except MissingBackend as error:
            return Response({
                "error": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:

            if isinstance(backend, BaseOAuth1):
                access_token = {
                    "oauth_token": serializer.data.get('access_token'),
                    "oauth_token_secret": serializer.data.get('access_token_secret')
                }
            elif isinstance(backend, BaseOAuth2):

                access_token = serializer.data.get('access_token')

            authenticated_user = backend.do_auth(access_token)

        except HTTPError as error:

            return Response({
                "error": "Http Error",
                "detail": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "detail": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            try:
                token = str(Token.objects.get(user=authenticated_user))
            except Token.DoesNotExist:
                token = str(Token.objects.create(user=authenticated_user))
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": token
            }

            return Response(status=status.HTTP_200_OK, data=response)
