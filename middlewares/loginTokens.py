from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect


class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request:HttpRequest):
        pathURL = request.path
        if "/admin/" in pathURL and not request.user.is_superuser:
            return redirect("home")
        respone = self.get_response(request)
        return respone