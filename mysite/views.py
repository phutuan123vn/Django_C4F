from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

import mysite.forms as forms
from utils.HTTPRequest import is_ajax
from utils.UserVerify import RedirectUser, user_verify


@method_decorator(RedirectUser(), name="dispatch")
class AccountCreateView(CreateView):
    form_class = forms.RegisterForm
    template_name = "index.html"
    success_url = "/"
    
    
    def form_valid(self, form):
        if is_ajax(self.request):
            return JsonResponse({"status": "success"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(form.errors)
    
    
@require_http_methods(["POST"])
def loginUser(request: HttpRequest):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if is_ajax(request):
        # print(user)
        if user is not None:
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"})
    login(request, user)
    if request.POST.get("next"):
        return redirect(request.POST.get("next"))
    return redirect("home")

@login_required(login_url="/account/")
def logoutUser(request: HttpRequest):
    logout(request)
    return redirect("/account/")
        

@method_decorator(user_verify, name="dispatch")
class HomeView(View):
    def get(self, request):
        # <view logic>
        return render(request, "home.html")
    
    def post(self, request):
        # <view logic>
        return HttpResponse("Home")

# def register(request):
#     if request.method == "POST":
#         # print(request.POST)
#         form = RegisterForm(data = request.POST)
#         if form.is_valid():
#             print("Clean Data",form.cleaned_data)
#             form.save()
#             return render(request, "base.html")
#         else:
#             pprint(dir(form.errors))
#             errors = form.errors
#             pprint(form.errors.values())
#             return render(request, "index.html", {"form": form, "errors": errors})
#     else: 
#         form = RegisterForm()
#     return render(request, "index.html", {"form": form})
