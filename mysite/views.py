from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from mysite.serializers import RegisterUserSerializer, UserSerializer, LoginUserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from mysite import settings
from django.middleware import csrf
from rest_framework import status
from rest_framework.permissions import AllowAny

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # print("token",refresh)
    # pprint(vars(refresh))
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    authentication_classes = ([])
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    
    def get(self, request: Request, format=None):
        return Response({"message":"Login page"})
    
    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if serializer.is_valid():
            user = serializer.validated_data
            if user:
                data = get_tokens_for_user(user)
                response = Response()
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["refresh"],
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
    authentication_classes = ([])
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

class LoginUserView(APIView):
    authentication_classes = ([])
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self,request: Request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            return Response(UserSerializer(User.objects.filter(username=serializer.validated_data).get()).data)
        return Response(serializer.errors)

@api_view(["GET","POST"])
def testAPI(request: Request):
    # access_token = ''
    # if request._auth['token_type'] == 'refresh':
    #     print(request.auth) 
    #     refreshTokenClass = RefreshToken(str(request.auth))
    #     access_token = str(refreshTokenClass.access_token)
    return Response({"message":"Hello World",
                        #  "access_token":access_token,
                    })