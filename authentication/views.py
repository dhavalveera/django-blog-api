from django.contrib.auth import authenticate, login as django_login, logout
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import CustomUser
from .serializer import UserLoginSerializer, UserRegistrationSerializer
from .helpers import get_tokens_for_user


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request=request.request, username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                if user.is_active:
                    user_data = CustomUser.objects.get(username=serializer.validated_data['username'])

                    token_data = get_tokens_for_user(user=user_data)

                    print(f"User from Django Authenticate => {user}")
                    print(f"Token => {token_data}")
                    return Response({'token': token_data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Sorry, your Account is not verified'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': "Invalid Credentials, Please check and re-try"},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def logout_view(request: Request):
    if request.method == 'POST':
        try:
            token_header = request.META.get('HTTP_AUTHORIZATION')
            bearer_token = token_header.replace("Bearer ", "")

            if bearer_token:
                token = RefreshToken(bearer_token)
                token.blacklist()
                print(f"User Logout Successfully!")
                return Response({'message': "Logout Successfully"}, status=status.HTTP_200_OK)
            else:
                print(f"User already Logout")
                return Response({'message': 'User already logged out'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Exception Executed for Logout with error: {e}')
            return Response({'message': "An Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)