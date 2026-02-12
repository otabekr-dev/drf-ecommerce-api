from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()

class RegisterView(APIView):


    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            user = User.objects.create(
                username = data.get('username'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
            )

            user.set_password(data['password'])
            user.save()

            return Response('User created', status=status.HTTP_201_CREATED)
        
class LoginView(APIView):

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            username = data.get('username')
            password = data.get('password')        

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response('User mavjud emas', status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return Response('Xato parol', status=status.HTTP_400_BAD_REQUEST)

            refresh_token = RefreshToken.for_user(user)
            return Response(
                {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token)
                }
            )    
