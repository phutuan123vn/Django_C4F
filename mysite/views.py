from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mysite.serializers import RegisterUserSerializer, UserSerializer


# @api_view(["POST"])
@csrf_exempt
def register(request: HttpRequest):
    serializer = RegisterUserSerializer(data=request.POST)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse(UserSerializer(user).data,safe=False)
    return JsonResponse(serializer.errors)