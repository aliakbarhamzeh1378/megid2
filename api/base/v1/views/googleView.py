import jwt
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.base.v1.models.userModel import UserModel
from api.base.v1.serializers.userSerializer import UserSerializer
from cas_server2 import settings


class GoogleAuthView(APIView):

    @swagger_auto_schema(
        operation_summary="Get Google Authorization URL",
        responses={200: openapi.Response("Authorization URL", schema=openapi.Schema(type="object", properties={"auth_url": openapi.Schema(type="string")}))}
    )
    def get(self, request):
        # Build the authorization URL
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        redirect_uri = request.build_absolute_uri(reverse('google-auth-callback'))
        scope = 'openid email profile'
        state = 'random_state_value'  # Replace with your own random string
        auth_url = f"{base_url}?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}"

        # Return the authorization URL as a JSON response
        return Response({'auth_url': auth_url})


class GoogleAuthCallbackView(APIView):
    def token_generator(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token
    @swagger_auto_schema(
        operation_summary="Handle Google Authorization Callback",
        manual_parameters=[
            openapi.Parameter(
                'code',
                openapi.IN_QUERY,
                description='Authorization code',
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def get(self, request):
        # Get the authorization code from the request
        code = request.GET.get('code')

        # Exchange the authorization code for tokens
        token_url = 'https://oauth2.googleapis.com/token'
        redirect_uri = request.build_absolute_uri(reverse('google-auth-callback'))
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=data)
        token_data = response.json()
        if response.status_code == 400:
            return Response(data='Login failed', status=status.HTTP_401_UNAUTHORIZED)
        # Verify the ID token
        id_token = token_data['id_token']
        jwt_info = jwt.decode(id_token, verify=False)

        # Verify the issuer and audience
        if jwt_info['iss'] != 'https://accounts.google.com' or jwt_info['aud'] != settings.GOOGLE_CLIENT_ID:
            # Invalid ID token
            # Handle the error as needed
            return Response(data='Login failed', status=status.HTTP_401_UNAUTHORIZED)
            pass
        user = UserModel.objects.filter(Email=jwt_info['email'])
        if user is None or len(user) == 0:

            return Response(data='Login failed', status=status.HTTP_401_UNAUTHORIZED)
        else:
            token = self.token_generator(user[0])
            serializer = UserSerializer(user[0])

            return Response(data={'token': token,
                                  'userInfo': serializer.data},
                            status=status.HTTP_200_OK)

        # Process the user data as needed
        # ...
