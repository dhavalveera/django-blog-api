from django.contrib.auth import authenticate, login as django_login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializer import UserLoginSerializer, UserRegistrationSerializer


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
                    django_login(request.request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'either Account is not Verified or Account is deleted'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': "Invalid Credentials, Please check and re-try"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request: Request):
    if request.method == 'POST':
        tkn = request.data.get('token')
        try:
            is_token_present = Token.objects.filter(key=tkn).delete()
            if is_token_present[0] == 0 and isinstance(is_token_present[1], dict) and not is_token_present[1]:
                return Response({'message': 'User already logged out'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logout(request=request.request)
                return Response({'message': 'Logout Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'Exception Executed for Logout with error: {e}')
            return Response({'message': "An Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)