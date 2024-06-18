from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from mysite.serializers import RegisterUserSerializer, UserSerializer, LoginUserSerializer
from django.contrib.auth.models import User
from rest_framework.mixins import RetrieveModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from mysite import settings
from django.contrib.auth import authenticate,login
from django.middleware import csrf
from rest_framework import status

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request: Request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","data":data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

class CreateUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

class LoginUserView(APIView):
    serializer_class = LoginUserSerializer


    def post(self,request: Request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response(UserSerializer(User.objects.get(username=serializer.validated_data['username'])).data)
        return Response(serializer.errors)



# @api_view(["GET","POST"])
def testAPI(request: Request):
    # serializer = RegisterUserSerializer(data=request.data)
    # if serializer.is_valid():
    #     user = serializer.save()
    #     return Response(UserSerializer(user).data)
    return JsonResponse({"message":"Hello World"})